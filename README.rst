#########
OpsGenie-Python
#########
**A Python client for the OpsGenie API**

Features
========
- Compatible with Python 3 (only)
- Provides wrappers around common API calls

Install
=======

.. code-block:: shell

    pip install opsgenie

Run the Tests
=============

.. code-block:: shell

    pip install tox
    git clone https://github.com/HurricaneLabs/opsgenie-python.git
    cd opsgenie-python
    tox

Examples
--------

Creating and Re-Assigning
======================

Try this out:

.. code-block:: python
    
    from opsgenie.api import OpsGenieAPI

    api_key = "your-api-key-here"
    api = OpsGenieAPI(api_key)

    alert = api.get_resource("alert")
    create_result = alert.create("test")
    print(create_result)
    print("\n")
    assign_result = alert.assign("Sam Johnson", alertId=create_result["alertId"])
    print(assign_result)
    print("\n")
    test_alert = alert.get(id=create_result["alertId"])
    print(test_alert)

The result should be something like this:

.. code-block:: json

    {"took": 166, "status": "successful", "alertId": "f75f423d-384b-4dc8-b040-f5d900507c5f", "code": 200, "message": "alert created"}


    {"took": 100, "status": "successful", "code": 200}


    {"took": 6, "source": "***REMOVED***", "message": "test", "actions": [], "count": 1, "id": "f75f423d-384b-4dc8-b040-f5d900507c5f", "recipients": [], "createdAt": 1430498993502001123, "isSeen": False, "tinyId": "1155", "alias": "f75f423d-384b-4dc8-b040-f5d900507c5f", "status": "open", "description": "", "tags": [], "owner": "Sam Johnson", "teams": [], "details": {}, "acknowledged": False, "updatedAt": 1430498993997001330, "entity": "", "systemData": {"integrationName": "Direct Notifications", "integrationId": "3be741a2-1bdd-4474-9046-c5539ce710d1", "integrationType": "API"}}
