{
  "kind": "python",
  "interface": {
    "begsim_intrpt": true,
    "endsim_intrpt": false,
    "failure_intrpts": false,
    "recovery_intrpts": false,
    "priority": 0,
    "super_priority": false
  },
  "attributes": [
    {
      "name": "role",
      "label": "角色",
      "type": "string",
      "desc": "",
      "unit": "",
      "validator": "",
      "defaultValue": "server",
      "symbolMap": [
        {
          "key": "服务端",
          "value": "server"
        },
        {
          "key": "客户端",
          "value": "client"
        }
      ],
      "allowOtherValues": true
    },
    {
      "name": "dest",
      "label": "目的地址",
      "type": "string",
      "desc": "",
      "unit": "",
      "validator": "",
      "defaultValue": "192.168.2.10",
      "symbolMap": [],
      "allowOtherValues": true
    }
  ],
  "graph": {
    "nodes": [
      {
        "id": "0c46c568-8bd6-4f00-8bda-1fc1cbe7100f",
        "name": "wait",
        "mandatory": false,
        "entryCreated": true,
        "exitCreated": false,
        "entryCode": "",
        "exitCode": "",
        "position": {
          "x": 210,
          "y": 240
        },
        "size": {
          "width": 96,
          "height": 96
        }
      },
      {
        "id": "48836461-a5fb-4683-86b4-0f059f52800d",
        "name": "idle",
        "mandatory": false,
        "entryCreated": true,
        "exitCreated": false,
        "entryCode": "",
        "exitCode": "",
        "position": {
          "x": 628.4480168765338,
          "y": 240
        },
        "size": {
          "width": 96,
          "height": 96
        }
      },
      {
        "id": "38d8548c-7352-4d2f-b415-c451caf06ff7",
        "name": "init",
        "mandatory": false,
        "entryCreated": true,
        "exitCreated": false,
        "entryCode": "",
        "exitCode": "",
        "position": {
          "x": 414.7653773380705,
          "y": 240
        },
        "size": {
          "width": 96,
          "height": 96
        }
      }
    ],
    "edges": [
      {
        "id": "19214e68-8b84-4722-b643-389d350ada1a",
        "source": {
          "cell": "0c46c568-8bd6-4f00-8bda-1fc1cbe7100f",
          "selector": "> circle:nth-child(1)"
        },
        "target": {
          "cell": "38d8548c-7352-4d2f-b415-c451caf06ff7"
        },
        "condition": "",
        "handlerCreated": true,
        "connector": "smooth",
        "vertices": [],
        "initialMarker": false
      },
      {
        "id": "97edbda3-9f77-4d46-a1a9-81f05247901b",
        "source": {
          "cell": "38d8548c-7352-4d2f-b415-c451caf06ff7",
          "selector": "> circle:nth-child(1)"
        },
        "target": {
          "cell": "48836461-a5fb-4683-86b4-0f059f52800d",
          "selector": "> circle:nth-child(1)"
        },
        "condition": "",
        "handlerCreated": true,
        "connector": "smooth",
        "vertices": [],
        "initialMarker": false
      },
      {
        "id": "e4ffa9f7-46c4-420b-b2c7-3975bdb231cb",
        "source": {
          "cell": "48836461-a5fb-4683-86b4-0f059f52800d",
          "selector": "> circle:nth-child(1)"
        },
        "target": {
          "cell": "48836461-a5fb-4683-86b4-0f059f52800d"
        },
        "condition": "",
        "handlerCreated": true,
        "connector": {
          "name": "smooth"
        },
        "vertices": [
          {
            "x": 734.4480168765338,
            "y": 235
          },
          {
            "x": 782.4480168765338,
            "y": 288
          },
          {
            "x": 734.4480168765338,
            "y": 341
          }
        ],
        "initialMarker": false
      }
    ],
    "initialStateId": null
  },
  "pythonPackageFiles": [
    "src/echo_app/__init__.py",
    "README.md",
    "pyproject.toml"
  ]
}
