const Node = {
  "id": "f0f1296cff0d9ac9",
  "type": "change",
  "z": "971a7ae6df987a48",
  "name": "set file data",
  "rules": [
    {
      "t": "set",
      "p": "payload",
      "pt": "msg",
      "to": "$.\"payload\".filedata",
      "tot": "jsonata"
    }
  ],
  "action": "",
  "property": "",
  "from": "",
  "to": "",
  "reg": false,
  "x": 1010,
  "y": 200,
  "wires": [
    [
      "5105b7b470e035f2"
    ]
  ]
}

module.exports = Node;