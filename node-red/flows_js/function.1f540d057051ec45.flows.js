const Node = {
  "id": "1f540d057051ec45",
  "type": "function",
  "z": "971a7ae6df987a48",
  "name": "decode file and add to request",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [
    {
      "var": "iconvLite",
      "module": "iconv-lite"
    }
  ],
  "x": 1350,
  "y": 200,
  "wires": [
    [
      "e2ea44fe64bb0d37"
    ]
  ]
}

Node.func = async function (node, msg, RED, context, flow, global, env, util, iconvLite) {
  let files = [];
  msg.payload.forEach(function (zipEntry) {
      files.push({ "filename":zipEntry.filename, "filedata": iconvLite.decode(zipEntry.payload, 'windows-1252', { stripBOM: false })});
  });
  
  // Only set first file from zip - name hardcoded for now
  msg.headers = {};
  msg.headers['Content-Type'] = 'multipart/form-data';
  msg.headers['Accept'] = 'application/json';
  msg.payload = {
      'file': {
          value: files[0].filedata,
          options: {
              filename: 'UTMBrændstof_2023.csv',
              contentType: 'text/csv'
          }
      }
  }
  
  return msg;
}

module.exports = Node;