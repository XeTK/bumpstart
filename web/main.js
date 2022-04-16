const API_ENDPOINT_SERVERS = "http://127.0.0.1:5000/api/servers";
const API_ENDPOINT_SERVER = "http://127.0.0.1:5000/api/server/";

const TABLE_ROW = (status, name, ip) => `
<tr>
    <th scope="row">${status}</th>
    <td>${name}</td>
    <td><a href="http://${ip}">Connect</a></td>
</tr>
`;

const TABLE_BUTTON = (server_name, next_state, classes, text) => `
<button type="button" 
    id="button_${server_name}"
    data-server-name="${server_name}"
    data-next-state="${next_state}"
    class="${classes}"
>${text}</button>
`

function on_power(event) {
    const server = event.target.dataset.serverName;
    const new_state = event.target.dataset.nextState;

    fetch(API_ENDPOINT_SERVER + server + '/' + new_state, { method: 'POST' })
        .then(data => alert("Changing state of " + server + ' to ' + new_state));
}

function add_server(server) {
    let server_id = server.id;

    fetch(API_ENDPOINT_SERVER + server_id)
        .then(response => response.json())
        .then(data => {
            const classes = (data.status) ? 'btn btn-on' : 'btn btn-off';
            const text = (data.status) ? 'Power Off' : 'Power On';
            const next_state = (data.status) ? 'off' : 'on';

            const button = TABLE_BUTTON(server_id, next_state, classes, text);
            const row = TABLE_ROW(button, server.name, server.ip);

            document.querySelector('#server_table_body')
                .insertAdjacentHTML("beforeend", row);
        
            document.querySelector(`#button_${server_id}`)
                .addEventListener('click', on_power)
        })
        .catch(error => console.error(error));
}

function main() {
    fetch(API_ENDPOINT_SERVERS)
        .then(response => response.json())
        .then(data => { 
            for (var server in data) 
                add_server(data[server]);
        });
}

document.addEventListener("DOMContentLoaded", main)