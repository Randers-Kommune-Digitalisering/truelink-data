const Node = {
  "id": "527932cb56a7269c",
  "type": "change",
  "z": "971a7ae6df987a48",
  "name": "set sftp env vars",
  "rules": [
    {
      "t": "set",
      "p": "port",
      "pt": "msg",
      "to": "SFTP_PORT",
      "tot": "env"
    },
    {
      "t": "set",
      "p": "user",
      "pt": "msg",
      "to": "SFTP_USER",
      "tot": "env"
    },
    {
      "t": "set",
      "p": "host",
      "pt": "msg",
      "to": "SFTP_HOST",
      "tot": "env"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 400,
  "y": 200,
  "wires": [
    [
      "956578d3751fb39c"
    ]
  ]
}

module.exports = Node;