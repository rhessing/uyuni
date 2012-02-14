<%@ taglib uri="http://rhn.redhat.com/rhn" prefix="rhn" %>
<%@ taglib uri="http://rhn.redhat.com/tags/list" prefix="rl" %>
<%@ taglib uri="http://jakarta.apache.org/struts/tags-html" prefix="html" %>
<%@ taglib uri="http://jakarta.apache.org/struts/tags-bean" prefix="bean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<rhn:toolbar base="h1" img="/img/susestudio.png"></rhn:toolbar>

<c:choose>
  <c:when test="${requestScope.errorMsg != null}">
    <div class="page-summary">
      <p><bean:message key="${requestScope.errorMsg}" /></p>
    </div>
  </c:when>

  <c:otherwise>
    <div class="page-summary">
      <p>Please choose one of the available images below for deployment to this virtual host.</p>
    </div>

    <rl:listset name="groupSet">
      <rhn:csrf />
      <html:hidden property="sid" value="${param.sid}" />

      <rl:list dataset="imagesList" emptykey="studio.images.list.noimages">
        <rl:radiocolumn value="${current.id}" styleclass="first-column"/>
        <rl:column headerkey="studio.images.list.name">
            <a href="${current.editUrl}">${current.name}</a>
        </rl:column>
        <rl:column headerkey="studio.images.list.version">
            ${current.version}
        </rl:column>
        <rl:column headerkey="studio.images.list.arch">
            ${current.arch}
        </rl:column>
        <rl:column headerkey="studio.images.list.type">
            ${current.imageType}
        </rl:column>
      </rl:list>

      <h2>Virtual Machine Setup</h2>
      <table class="details" align="center">
        <tr>
          <th>Number of VCPUs:</th>
          <td>
            <html:text property="vcpus" value="1" />
          </td>
        </tr>
        <tr>
          <th>Memory (MB):</th>
          <td>
            <html:text property="mem_mb" value="512" />
          </td>
        </tr>
        <tr>
          <th>Bridge Device:</th>
          <td>
            <html:text property="bridge" value="br0" />
          </td>
        </tr>
      </table>

      <h2>Proxy Configuration (Optional)</h2>
      <table class="details" align="center">
        <tr>
          <th>Proxy Server:</th>
          <td>
            <html:text property="proxy_server" value="" />
          </td>
        </tr>
        <tr>
          <th>Proxy User:</th>
          <td>
            <html:text property="proxy_user" value="" />
          </td>
        </tr>
        <tr>
          <th>Proxy Password:</th>
          <td>
            <html:password property="proxy_pass" value="" />
          </td>
        </tr>
      </table>

      <div align="right">
        <rhn:submitted />
        <hr />
        <html:submit
            property="dispatch"
            value="Schedule Deployment"
            disabled="${empty requestScope.imagesList}" />
      </div>
    </rl:listset>
  </c:otherwise>
</c:choose>
