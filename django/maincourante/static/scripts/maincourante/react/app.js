const Modal = ReactBootstrap.Modal;
const OverlayTrigger = ReactBootstrap.OverlayTrigger;
const Button = ReactBootstrap.Button;
const Panel = ReactBootstrap.Panel;

class MessageReplyForm extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            id: props.message.id,
            body: props.message.body,
            evenement: props.message.evenement,
            modified: props.message.modified,
            operateur: props.message.operateur,
            receiver: props.message.receiver,
            resource_uri: props.message.resource_uri,
            sender: props.message.sender,
            timestamp: props.message.timestamp,
            edit: props.message.edit,
            reply: props.message.reply,
            responseBody: props.message.responseBody
        };

    }
    handleSubmit(e) {
        e.preventDefault();
        const formData = {};
        formData["body"] = this.refs["body"].value;
        formData["sender"] = this.refs["receiver"].value;
        formData["receiver"] = this.refs["sender"].value;
        formData["evenement"] = "test";
        var entry_point = api_url + 'message/';
        var loadUrl = entry_point;
        fetch(loadUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "same-origin",
            body: JSON.stringify(formData)
        })
            .then((response) => {
                if (response.status >= 400) {
                    throw new Error("Bad response from server");
                }
                return response.json();
            })
            .then((data) => {
                this.props.addMessage(data);
                this.close();
            });
    }
    handleKeyPress(event) {
        if (event.key == 'Enter') {
            console.log('enter press here! ')
        }
        console.log(event.key)
    }
    close() {
        this.props.close();
    }
    handleKeyPress(event) {
        if (event.key == 'Enter') {
            console.log('enter press here! ')
        }
        console.log(event.key)
    }
    render() {
        return (
            <div>
                <Modal show={this.props.message.reply} onHide={this.close.bind(this)}>
                    <Modal.Header closeButton>
                        <Modal.Title>Ecrire une réponse</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div className="row">
                            <form onSubmit={this.handleSubmit}>
                                <div className="form-group">
                                    <label className="col-md-3 control-label">Destinataire</label>
                                    <div className="col-md-9">
                                        <input disabled className="form-control" onKeyPress={this.handleKeyPress.bind(this)} ref="receiver" type='text' name="receiver" value={this.state.receiver} />
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label className="col-md-3 control-label">Expéditeur</label>
                                    <div className="col-md-9">
                                        <input disabled className="form-control" onKeyPress={this.handleKeyPress.bind(this)} ref="sender" type='text' name="sender" value={this.state.sender} />
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="col-md-3 control-label">Message</label>
                                    <div className="col-md-9">
                                        <input disabled className="form-control" onKeyPress={this.handleKeyPress.bind(this)} ref="source" type='text' name="source" value={this.state.body} />
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="col-md-3 control-label">Réponse</label>
                                    <div className="col-md-9">
                                        <input className="form-control" onKeyPress={this.handleKeyPress.bind(this)} ref="body" type='text' name="body" />
                                    </div>
                                </div>
                            </form>
                        </div>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button bsStyle="primary" onClick={this.handleSubmit.bind(this)}>Envoyer</Button>
                        <Button bsStyle="warning" onClick={this.close.bind(this)}>Close</Button>
                    </Modal.Footer>
                </Modal>

            </div>
        );
    }
}


class MessageForm extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleSubmit(e) {
        e.preventDefault();
        const formData = {};
        for (const field in this.refs) {
            formData[field] = this.refs[field].value;
        }
        formData["evenement"] = "test";
        this.createNewMessage(formData);
        
    }

    createNewMessage(newMessage){
        var entry_point = api_url + 'message/';
        var loadUrl = entry_point;
        fetch(loadUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "same-origin",
            body: JSON.stringify(newMessage)
        })
            .then((response) => {
                if (response.status >= 400) {
                    throw new Error("Bad response from server");
                }
                return response.json();
            })
            .then((data) => {
                this.props.addMessage(data);
                if(newMessage.response){
                    newMessage.body = newMessage.response;
                    newMessage.response = null;
                    newMessage.receiver = data.sender;
                    newMessage.sender = data.receiver;
                    this.createNewMessage(newMessage);
                }
            });
    }

    handleKeyPress(event) {
        if (event.key == 'Enter') {
            console.log('enter press here! ')
        }
        console.log(event.key)
    }

    render() {
        return (
            <div className="panel panel-primary">
                <div className="panel-heading">
                    <h4>Saisie des messages</h4>
                </div>
                <div className="panel-body panel-body-md">
                    <form className="form-horizontal" onSubmit={this.handleSubmit}>
                        <div className="form-group">
                            <label className="col-md-3 control-label">Destinataire</label>
                            <div className="col-md-9">
                                <input className="form-control" onKeyPress={this.handleKeyPress.bind(this)} ref="receiver" type='text' name="receiver" placeholder="Destinataire" />
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="col-md-3 control-label">Expéditeur</label>
                            <div className="col-md-9">
                                <input className="form-control" onKeyPress={this.handleKeyPress.bind(this)} ref="sender" type='text' name="sender" placeholder="Expéditeur" />
                            </div>
                        </div>

                        <div className="form-group">
                            <label className="col-md-3 control-label">Message</label>
                            <div className="col-md-9">
                                <input className="form-control" onKeyPress={this.handleKeyPress.bind(this)} ref="body" type='text' name="body" placeholder="Message" />
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="col-md-3 control-label">Réponse</label>
                            <div className="col-md-9">
                                <input className="form-control" onKeyPress={this.handleKeyPress.bind(this)} ref="response" type='text' name="response" placeholder="Réponse" />
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-md-9 col-md-offset-3">
                                <button type="submit" onClick={this.handleSubmit.bind(this)} className="btn btn-primary">Envoyer</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        );
    }
}

class Message extends React.Component {
    constructor(props) {
        super(props);
        this.submitUpdate = this.submitUpdate.bind(this);
        this.state = {
            id: props.message.id,
            body: props.message.body,
            evenement: props.message.evenement,
            modified: props.message.modified,
            operateur: props.message.operateur,
            receiver: props.message.receiver,
            resource_uri: props.message.resource_uri,
            sender: props.message.sender,
            timestamp: props.message.timestamp,
            edit: false,
            reply: false,
            new: true
        };
    }
    editMessage() {
        this.setState({ edit: true });
    }
    replyMessage() {
        this.setState({ reply: true });
    }
    closeReplyMessage() {
        this.setState({ reply: false });
    }
    cancelEdition() {
        this.setState({ edit: false });
    }
    submitUpdate() {
        var entry_point = api_url + 'message/';
        var loadUrl = entry_point + this.state.id;
        fetch(loadUrl, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "same-origin",
            body: JSON.stringify(this.state)
        })
            .then((response) => {
                console.log(response);
                if (response.status >= 400) {
                    throw new Error("Bad response from server");
                }
                return response.json();
            })
            .then((data) => {
                this.props.message.body = this.state.body;
                this.setState({ edit: false });
            });
    }
    renderHeader() {
        let warning = null;
        let buttons = null;
        const editionMode = true;
        if (this.props.message.deleted == true || this.props.message.modified == true) {
            let warningMessage = null;
            if (this.props.message.deleted == true && this.props.message.modified == true) {
                warningMessage = "Message modifié puis supprimé";
            } else if (this.props.message.modified) {
                warningMessage = "Message modifié";
            } else if (this.props.message.deleted) {
                warningMessage = "Message supprimé";
            }
            warning = <span className="text-danger"><span className="glyphicon glyphicon-warning-sign"></span>{warningMessage}</span>
        }
        if (editionMode) {
            let editButton = null;
            let deleteButton = null;
            let replyButton = null;
            replyButton = <a className="btn btn-primary btn-xs" onClick={this.replyMessage.bind(this)}><span className="glyphicon glyphicon-share-alt"></span></a>
            if (!this.state.edit) {
                if (!this.props.message.deleted) {
                    editButton = <a className="btn btn-primary btn-xs" onClick={this.editMessage.bind(this)} ><span className="glyphicon glyphicon-edit"></span></a>
                    deleteButton = <a className="btn btn-danger btn-xs"><span className="glyphicon glyphicon-trash"></span></a>
                }
            } else {
                editButton = <a className="btn btn-success btn-xs" onClick={this.submitUpdate.bind(this)}><span className="glyphicon glyphicon-ok"></span>Valider</a>
                deleteButton = <a className="btn btn-warning btn-xs" onClick={this.cancelEdition.bind(this)}><span className="glyphicon glyphicon-remove"></span>Annuler</a>
            }
            buttons = <span>{replyButton}{editButton}{deleteButton}</span>
        }
        return <div className="panel-heading panel-heading-sm">{moment(this.props.message.timestamp).format("DD MMM YYYY à HH:mm:ss")} <b>| {this.props.message.receiver} </b> de <b>{this.props.message.sender} </b> | message saisi par <b>{this.props.message.operateur}</b>
            <div className="pull-right">
                {warning}
                {buttons}
            </div>
            <MessageReplyForm message={this.state} close={this.closeReplyMessage.bind(this)} addMessage={this.props.addMessage.bind(this)} />
        </div>;
    }
    handleChange(event) {
        this.setState({ body: event.target.value });
    }
    handleKeyPress(event) {
        if (event.key == 'Enter') {
            this.submitUpdate();
        }
    }
    render() {
        const header = this.renderHeader();
        let body = null;
        let panelClass = "panel panel-sm ";
        if(this.props.message.deleted){
            panelClass += "panel-default"
        }else if (this.props.message.new){
            panelClass += "panel-success"
        }else{
            panelClass += "panel-info"
        }
        if (this.state.edit) {
            body = <div><input type="text" className="form-control" ref="message.body" value={this.state.body} onChange={this.handleChange.bind(this)} onKeyPress={this.handleKeyPress.bind(this)}></input></div>
        } else {
            body = <div>{this.props.message.body}</div>;
        }
        return <div className={panelClass}>
            {header}
            <div className="panel-body panel-body-sm">
                {body}
            </div>
        </div>;
    }
}

class MessageList extends React.Component {
    componentDidMount() {
        this.timer = setInterval(this.getNewMessages.bind(this), 12000);
        this.getNewMessages();
    }
    componentWillUnmount() {
        clearInterval(this.timer);
    }
    getNewMessages() {
        var entry_point = api_url + 'message/';
        var loadUrl = entry_point + "?format=json&limit=0&evenement=" + EVENEMENT_ID;
        if (this.lastTimestamp) {
            loadUrl += "&newer-than=" + this.lastTimestamp;
        }
        fetch(loadUrl, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            credentials: "same-origin"
        })
            .then(function (response) {
                if (response.status >= 400) {
                    throw new Error("Bad response from server");
                }
                return response.json();
            })
            .then((data) => {
                this.props.addMessages(data.messages);
            });
        this.lastTimestamp = moment().format("YYYY-MM-DDTHH:mm:ss.SSS");
    }
    render() {
        return <div>{this.props.messages.map((message, i) => <div key={message.id}> <Message message={message} addMessage={this.props.addMessage} /></div>)} </div>;
    }
};


class MessagePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = { messages: [] };
    }
    componentDidMount() {
        window.addEventListener('focus', this.focus.bind(this), false);
    }
    addMessage(newMessage) {
        const index = this.state.messages.findIndex((existingMessage) => newMessage.id == existingMessage.id);
        if (index == -1) {
            newMessage.new = true;
            this.state.messages.splice(0, 0, newMessage)
            //this.state.messages.push(newMessage);
        } else {
            this.state.messages.splice(index, 1, newMessage);
        }
        this.setState(this.state.messages);
    }
    sortByDate(a, b) {
        return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    }
    focus(){
        setTimeout(function() { 
                this.state.messages.forEach((message) => message.new = false);
                this.setState(this.state.messages);
            }.bind(this), 3000);
    }
    addMessages(newMessages) {
        if (this.state.messages.length == 0) {
            this.setState({ messages: newMessages.concat(this.state.messages) });
        } else {
            newMessages.forEach((newMessage) => this.addMessage(newMessage));
        }
    }
    render() {
        return <div>
            <div>
                <MessageForm addMessage={this.addMessage.bind(this)} />
            </div>
            <div className="panel panel-default">
                <div className="panel-body">
                    <MessageList messages={this.state.messages} addMessages={this.addMessages.bind(this)} addMessage={this.addMessage.bind(this)} />
                </div>
            </div>
        </div>;
    }
}

ReactDOM.render(
    <MessagePage />,
    document.getElementById('container')
);
