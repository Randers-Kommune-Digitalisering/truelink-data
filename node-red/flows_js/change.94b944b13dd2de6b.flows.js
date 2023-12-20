const Node = {
  "id": "94b944b13dd2de6b",
  "type": "change",
  "z": "971a7ae6df987a48",
  "name": "set files",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "{\"filename\": \"demo/\" & $.\"payload\"[0].name}",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 700,
  "y": 200,
  "wires": [
    [
      "4e41a97363bbe26b"
    ]
  ]
}

module.exports = Node;