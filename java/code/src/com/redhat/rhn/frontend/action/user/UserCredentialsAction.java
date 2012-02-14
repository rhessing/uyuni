/**
 * Copyright (c) 2012 Novell
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
package com.redhat.rhn.frontend.action.user;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.struts.action.ActionErrors;
import org.apache.struts.action.ActionForm;
import org.apache.struts.action.ActionForward;
import org.apache.struts.action.ActionMapping;
import org.apache.struts.action.ActionMessage;
import org.apache.struts.action.ActionMessages;

import com.redhat.rhn.domain.credentials.Credentials;
import com.redhat.rhn.domain.credentials.CredentialsFactory;
import com.redhat.rhn.domain.user.User;
import com.redhat.rhn.frontend.struts.RequestContext;
import com.redhat.rhn.frontend.struts.RhnAction;

/**
 * Configuration of credentials for external APIs like e.g. SUSE Studio.
 */
public class UserCredentialsAction extends RhnAction {

    private static String ATTRIB_CREDS = "creds";
    private static String PARAM_USER = "studioUser";
    private static String PARAM_KEY = "studioKey";
    private static String PARAM_URL = "studioUrl";

    /** {@inheritDoc} */
    @Override
    public ActionForward execute(ActionMapping mapping, ActionForm formIn,
            HttpServletRequest request, HttpServletResponse response)
    throws Exception {
        RequestContext ctx = new RequestContext(request);

        // Lookup this user's credentials
        User user = ctx.getCurrentUser();
        Credentials creds = CredentialsFactory.lookupByUser(user);
        if (creds == null) {
            // Create new credentials if necessary
            creds = CredentialsFactory.createNewCredentials(user);
            creds.setType(Credentials.TYPE_STUDIO);
        }
        request.setAttribute(ATTRIB_CREDS, creds);

        if (ctx.isSubmitted()) {
            // The form was submitted
            Credentials newCreds = CredentialsFactory.createNewCredentials(user);
            newCreds.setUsername(request.getParameter(PARAM_USER).trim());
            newCreds.setPassword(request.getParameter(PARAM_KEY).trim());
            newCreds.setUrl(request.getParameter(PARAM_URL).trim());

            // Check for completeness
            if (newCreds.isEmpty() || newCreds.isComplete()) {
                if (newCreds.isEmpty()) {
                    // Delete from DB
                    CredentialsFactory.removeCredentials(creds);
                    request.setAttribute(ATTRIB_CREDS, newCreds);
                } else {
                    // Store the credentials
                    creds.setUsername(newCreds.getUsername());
                    creds.setPassword(newCreds.getPassword());
                    creds.setUrl(newCreds.getUrl());
                    CredentialsFactory.storeCredentials(creds);
                }
                ActionMessages messages = new ActionMessages();
                messages.add(ActionMessages.GLOBAL_MESSAGE, new ActionMessage(
                        "yourcredentials.message.updated"));
                getStrutsDelegate().saveMessages(request, messages);
            } else {
                // Incomplete credentials, show an error
                ActionErrors errors = new ActionErrors();
                errors.add(ActionMessages.GLOBAL_MESSAGE,
                        new ActionMessage("yourcredentials.message.incomplete"));
                getStrutsDelegate().saveMessages(request, errors);
                request.setAttribute(ATTRIB_CREDS, newCreds);
            }
        }
        return mapping.findForward("default");
    }
}
