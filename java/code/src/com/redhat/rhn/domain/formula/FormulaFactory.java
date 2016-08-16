/**
 * Copyright (c) 2015 SUSE LLC
 *
 * This software is licensed to you under the GNU General Public License,
 * version 2 (GPLv2). There is NO WARRANTY for this software, express or
 * implied, including the implied warranties of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
 * along with this software; if not, see
 * http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
 *
 * Red Hat trademarks are not licensed under GPLv2. No permission is
 * granted to use or replicate Red Hat trademarks that are incorporated
 * in this software or its documentation.
 */
package com.redhat.rhn.domain.formula;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.FileAlreadyExistsException;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.apache.log4j.Logger;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.SafeConstructor;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.redhat.rhn.common.hibernate.HibernateFactory;
import com.redhat.rhn.domain.org.OrgFactory;
import com.redhat.rhn.domain.server.ManagedServerGroup;
import com.redhat.rhn.domain.server.ServerFactory;
import com.suse.manager.webui.controllers.ECMAScriptDateAdapter;

/**
 * Factory class for working with formulas.
 */
public class FormulaFactory extends HibernateFactory {

    private static Logger log = Logger.getLogger(FormulaFactory.class);
    private static FormulaFactory singleton = new FormulaFactory();
    private static final String FORMULA_DATA_DIRECTORY = "/srv/susemanager/formulas_data/";
    private static final String FORMULA_DIRECTORY = "/usr/share/susemanager/salt/formulas/";
    private static final Gson GSON = new GsonBuilder()
            .registerTypeAdapter(Date.class, new ECMAScriptDateAdapter())
            .serializeNulls()
            .create();
    private static final Yaml yaml = new Yaml(new SafeConstructor());

    private FormulaFactory() {
    }
    
    // Code for using hibernate and a database to save formula data
//    /**
//     * Save a {@link Formula}.
//     * @param formula the formula to save
//     */
//    public static void save(Formula formula) {
//        singleton.saveObject(formula);
//    }
//    
//    /**
//     * Get a {@link Formula} object from the db by serverId
//     * @param serverId the serverId
//     * @param orgId the org id
//     * @return an {@link Optional} containing a {@link Formula} object
//     */
//    public static Optional<Formula> getFormulaByServerId(long orgId, Long serverId) {
//        Formula formula = (Formula) getSession().createCriteria(Formula.class)
//                .add(Restrictions.eq("serverId", serverId))
//                .add(Restrictions.eq("org.id", orgId))
//                .uniqueResult();
//        return Optional.ofNullable(formula);
//    }

    
    public static void saveServerFormula(Map<String, Object> formData, Long serverId, String formulaName) throws IOException {
    	File formula_file = new File(FORMULA_DATA_DIRECTORY + "pillar/" + serverId + "_" + formulaName + ".json");
    	try {
    		formula_file.getParentFile().mkdirs();
			formula_file.createNewFile();
    	} catch (FileAlreadyExistsException e) {}
    	
    	BufferedWriter writer = new BufferedWriter(new FileWriter(formula_file));
    	writer.write(GSON.toJson(formData));
    	writer.close();
    	/*
    	Map<String, Object> content = GSON.fromJson(formula.getContent(), Map.class);
    	content.put("form_id", formula.getFormulaName());
    	writer.write("{\"formula\": ");
    	writer.newLine();
    	writer.write(GSON.toJson(content));
    	writer.newLine();
    	writer.write("}");*/
    }

    //OLD
    public static void deleteServerFormula(Long serverId) throws IOException {
    	File formula_file = new File(FORMULA_DATA_DIRECTORY + "pillar/" + ServerFactory.lookupById(serverId).getName() + ".json");
    	if (formula_file.exists()) {
    		formula_file.delete();
    	}
    }

    //OLD
    public static Optional<Formula> getFormulaByServerId(long orgId, Long serverId) {
    	File formula_file = new File(FORMULA_DATA_DIRECTORY + "pillar/" + ServerFactory.lookupById(serverId).getName() + ".json");
    	if (!formula_file.exists() || !formula_file.isFile())
    		return Optional.empty();
    	
    	try {
	    	FileInputStream fis = new FileInputStream(formula_file);
	        byte[] formula_file_data = new byte[(int) formula_file.length()];
	        fis.read(formula_file_data);
	        fis.close();
	        String file_content = new String(formula_file_data, "UTF-8");
	        Map<String, Object> map = (Map<String, Object>) GSON.fromJson(file_content, Map.class);
	        Map<String, Object> content = (Map<String, Object>) map.get("formula");
	        
	        Formula formula = new Formula();
	    	formula.setOrg(OrgFactory.lookupById(orgId));
	    	formula.setServerId(serverId);
	        formula.setFormulaName((String) content.remove("form_id"));
	    	formula.setContent(GSON.toJson(content));
	    	return Optional.of(formula);
    	}
    	catch (IOException e) {
    		return Optional.empty();
    	}
    }
    
    public static String[] listServerFormulas(Long serverId) {
    	LinkedList<String> formulas = new LinkedList<>();
    	File server_formulas_file = new File(FORMULA_DATA_DIRECTORY + "group_formulas.json");
    	if (!server_formulas_file.exists())
    		return new String[0];
    	
    	try {
			Map<String, List<String>> server_formulas = (Map<String, List<String>>) GSON.fromJson(new BufferedReader(new FileReader(server_formulas_file)), Map.class);
			
			for (ManagedServerGroup group : ServerFactory.lookupById(serverId).getManagedGroups())
				formulas.addAll(server_formulas.getOrDefault(group.getId().toString(), new ArrayList<>(0)));
	    	return formulas.toArray(new String[0]);
    	}
    	catch (FileNotFoundException e) {
    		return new String[0];
    	}
    }
    
    public static Optional<Map<String, Object>> getFormulaLayoutByName(String name) {
    	File layout_file = new File(FORMULA_DIRECTORY + name + "/form.yml");
    	
    	try {
			if (layout_file.exists())
				return Optional.of((Map<String, Object>) yaml.load(new FileInputStream(layout_file)));
			else {
		    	layout_file = new File(FORMULA_DIRECTORY + name + "/form.json");
		    	
		    	if (layout_file.exists())
		        	return Optional.of((Map<String, Object>) GSON.fromJson(new BufferedReader(new FileReader(layout_file)), Map.class));
		    	else
		    		return Optional.empty();
			}
    	} catch (FileNotFoundException e) {
    		return Optional.empty();
    	}
    }
    
    public static Optional<Map<String, Object>> getFormulaValuesByNameAndServerId(String name, Long serverId) {
    	File data_file = new File(FORMULA_DATA_DIRECTORY + "pillar/" + serverId + "_" + name + ".json");
    	try {
			if (data_file.exists())
				return Optional.of((Map<String, Object>) GSON.fromJson(new BufferedReader(new FileReader(data_file)), Map.class));
			else
		    	return Optional.empty();
    	} catch (FileNotFoundException e) {
    		return Optional.empty();
    	}
    }
    
    public static String[] getFormulasByServerGroupId(Long groupId) {
    	File group_formulas_file = new File(FORMULA_DATA_DIRECTORY + "group_formulas.json");
    	if (!group_formulas_file.exists())
    		return new String[0];
    	
    	// Read group_formulas file
    	try {
			Map<String, List<String>> server_formulas = (Map<String, List<String>>) GSON.fromJson(new BufferedReader(new FileReader(group_formulas_file)), Map.class);
			if (server_formulas.containsKey(groupId.toString()))
				return server_formulas.get(groupId.toString()).toArray(new String[0]);
			else
				return new String[0];
    	}
    	catch (IOException e) {
    		return new String[0];
    	}
    }
    
    // TODO: Needs update!
    public static void saveServerGroupFormulas(String serverGroupId, String selectedFormula) throws IOException {
    	File server_formulas_file = new File(FORMULA_DATA_DIRECTORY + "group_formulas.json");
    	
    	Map<String, String> server_formulas;
    	if (!server_formulas_file.exists()) {
    		server_formulas_file.getParentFile().mkdirs();
    		server_formulas_file.createNewFile();
    		server_formulas = new HashMap<String, String>();
    	}
    	else {
	    	// Read server_formulas file
	    	FileInputStream fis = new FileInputStream(server_formulas_file);
	        byte[] server_formulas_file_data = new byte[(int) server_formulas_file.length()];
	        fis.read(server_formulas_file_data);
	        fis.close();
			server_formulas = (Map<String, String>) GSON.fromJson(new String(server_formulas_file_data, "UTF-8"), Map.class);
    	}
		// Save selected Formula
		server_formulas.put(serverGroupId, selectedFormula);
		
		// Write server_formulas file
    	BufferedWriter writer = new BufferedWriter(new FileWriter(server_formulas_file));
    	writer.write(GSON.toJson(server_formulas));
    	writer.close();
    }
    
    /**
     * {@inheritDoc}
     */
    @Override
    protected Logger getLogger() {
        return log;
    }
}
