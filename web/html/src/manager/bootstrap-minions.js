'use strict';

const React = require("react");
const ReactDOM = require("react-dom");
const Panel = require("../components/panel").Panel;
const Messages = require("../components/messages").Messages;
const Network = require("../utils/network");
const AsyncButton = require("../components/buttons").AsyncButton;
const LinkButton = require("../components/buttons").LinkButton;

var BootstrapMinions = React.createClass({

    getInitialState: function() {
        return {
            host: "",
            user: "root",
            password: "linux"
        };
    },

    hostChanged: function(event) {
        this.setState({
            host: event.target.value
        });
    },

    userChanged: function(event) {
        this.setState({
            user: event.target.value
        });
    },

    passwordChanged: function(event) {
        this.setState({
            password: event.target.value
        });
    },

    onBootstrap: function() {
        var formData = {};
        formData['host'] = this.state.host.trim();
        formData['user'] = this.state.user.trim();
        formData['password'] = this.state.password.trim();

        const request = Network.post(
            window.location.href,
            JSON.stringify(formData),
            "application/json"
        ).promise.then(data => {
            this.setState({
                success: data.success,
                errors: null
            });
            if (!data.success) {
                this.setState({
                    errors: [data.errorMessage]
                });
            }
        }, (xhr) => {
            try {
                this.setState({
                    errors: JSON.parse(xhr.responseText)
                })
            } catch (err) {
                this.setState({
                    errors: Network.errorMessageByStatus(xhr.status)
                })
            }
        });
        return request;
    },

    render: function() {
        var errs = null;
        if (this.state.errors) {
            errs = <Messages items={this.state.errors.map(function(error) {
                return {severity: "error", text: error};
            })}/>;
        }

        var msg = null;
        if (this.state.success) {
            msg = <Messages items={[{severity: "info", text: t("Successfully bootstrapped host!")}]}/>;
        }

        var buttons = [];
        buttons.push(
            <AsyncButton id="bootstrap-btn" icon="plus" name={t("Bootstrap")} action={this.onBootstrap}/>
        );
        buttons.push(
            <LinkButton id="cancel-btn" className="btn-default pull-right" text={t("Back to System Overview")} href="/rhn/systems/Overview.do"/>
        );

        return (
        <Panel title={t("Bootstrap Minions")} icon="spacewalk-icon-salt-add">
            {errs}
            {msg}
            <div className="form-horizontal">
                <div className="form-group">
                    <label className="col-md-3 control-label">Host:</label>
                    <div className="col-md-6">
                        <input name="hostname" className="form-control" type="text" placeholder={t("IP address or DNS name")} onChange={this.hostChanged}/>
                    </div>
                </div>
                <div className="form-group">
                    <label className="col-md-3 control-label">User:</label>
                    <div className="col-md-6">
                        <input name="user" className="form-control" type="text" defaultValue={this.state.user} onChange={this.userChanged}/>
                    </div>
                </div>
                <div className="form-group">
                    <label className="col-md-3 control-label">Password:</label>
                    <div className="col-md-6">
                        <input name="password" className="form-control" type="password" defaultValue={this.state.password} onChange={this.passwordChanged}/>
                    </div>
                </div>
                <div className="form-group">
                    <div className="col-md-offset-3 col-md-6">
                        {buttons}
                    </div>
                </div>
            </div>
        </Panel>
        )
    }
});

ReactDOM.render(
  <BootstrapMinions />,
  document.getElementById('bootstrap-minions')
);
