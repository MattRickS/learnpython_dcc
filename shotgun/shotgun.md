# Shotgun API

Shotgun has it's own API that you need to download and install to use. See the following links for instructions.

- https://developer.shotgunsoftware.com/python-api/
- https://developer.shotgunsoftware.com/python-api/reference.html#shotgun-methods

# Login
To connect to shotgun via the API you need to use the URL of the site, and the login credentials for either a HumanUser (eg, yourself) or a ScriptUser (a special permissions user created to run scripts only). You need admin privileges to setup a ScriptUser, so unless you know the login details for one already, you'll have to login using your own credentials.
```python
URL = "https://STUDIO.shotgunstudio.com"
```
For example, if your studio was called "Cool Films" your url might be `https://coolfilms.shotgunstudio.com`.

### HumanUser
Takes your usual shotgun login name and password. Be careful not to sure the file with your password with anyone!
```python
login = "mshaw"
password = "PASSWORD"  # Not my real password in case you're wondering
sg = shotgun_api3.Shotgun(URL, login=login, password=password)
```

### ScriptUser
Takes the specific script name and "api key", ie, a script password.
```python
script_name = "my_edit_script"
api_key = "SUPER SECRET KEY"
sg = shotgun_api3.Shotgun(URL, script_name=script_name, api_key=api_key)
```

# Schema
Using the API, you can do anything the logged in user could do, such as viewing, editing, or creating "entities". Everything you see on shotgun is an "Entity", eg, "Asset", "Shot", "Version", etc... An entity is represented in python by a dictionary with at least two keys:
- "type" must have a value of the entity type, eg, "Asset"
- "id" is an integer for the unique identifier of the entity. The first asset created is 1, the second is 2, etc...

So an entity might look like this: `{"type": "Asset", "id": 1}`

Entities also have many fields, like the ones you can see on shotgun. This could also be included in the dictionary,
but the names might not match what you see on shotgun. For example, an asset name is not a field called "name" but
instead a field called "code". In fact, most entities use the field name "code" for the name you recognise, with a few
exceptions.

`{"type": "Asset", "id": 1, "code": "TheAssetName", "shots": [{"type": "Shot", "id": 2},]}`

The fields an entity has are called it's "schema". To see the schema, you can call the schema methods from shotgun.
Each field also has some information about it, such as whether it is editable, etc..

```python
# Gets ALL entities schemas
schemas = sg.schema_read()
# {"Asset": {"code": {...}, "id": {...}}, ...}

# Gets a specific entity's schema, eg, Asset
asset_schema = sg.schema_field_read("Asset")
# {"code": {...}, "id": {...}}
```

# Operations
All operations require the logged in API user (Human / Script) to have the permissions assigned or it will raise an error. If you're logged in as your own user, you'll be able to do anything you can do in the UI. Hopefully whoever manages your shotgun instance has set the correct permissions for you, but be careful - you may have more access than you might think (don't accidentally delete the current studio project!).

## Find
Reading data from the database is done with the "find" or "find_one". It takes three common arguments:
- entity_type: the entity type to look for
- filters: Shotgun's filter syntax: https://developer.shotgunsoftware.com/python-api/reference.html#filter-syntax
- fields: A list of field names to return for each entity. "type" and "id" are always returned.

The following example finds all Assets that match ALL the filters, and returns each with the type, id, and code fields.
```python
filters = [
    # field name,  comparison,  value(s)
    ["sg_asset_type", "is", "Character"],  # Character assets
    ["sg_status_list", "in", ["ip", "wtg"]],  # Status is either "In Progress" or "Waiting to Start"
    ["project", "is", {"type": "Project", "id": 1}]  # Entity fields can be queried by using a dict of "type" and "id"
]
fields = ["code"]
entities = sg.find("Asset", filters, fields=fields)
# [{"type": "Asset", "id": 1, "code": "AssetName1"}, {"type": "Asset", "id": 2, "code": "AssetName2"}]
```

### Field hopping
Field hopping is a way of identifying values on entities linked to the entity you're querying. This can be used for fields to filter by, or for requesting fields in the result. The syntax is: `field_name.EntityType.field_name`

An example: Shot has it's Sequence as a field (sg_sequence), so to query the sequence name (field name: code) you can use the field hopping value: `sg_sequence.Sequence.code`

```python
filters = [
    ["project.Project.name", "is", "My Project"],  # This entities project field's id
    ["sg_sequence.Sequence.code", "is", "sq0100"]  # This entities sg_sequence field's "code" field
]
fields = ["code", "sq_sequence"]
shot = sg.find_one("Shot", filters, fields=fields)
# {"type": "Shot", "id": 1, "code": "s0100", "sg_sequence": {"type": "Sequence", "id": 1}}
```

## Create
**WARNING: This operation is actually modifying the data on the site. Make sure you are only modifying entities that are safe to do so with.**

To create a new entity, you must provide at least all required fields. See the schema to know what's required. Shotgun will raise an error if anything is wrong.

An example to create a new project:
```python
project = sg.create("Project", {"code": "myProject", "name": "My Project"})
# {"type": "Project", "id": 1}
```

## Update
**WARNING: This operation is actually modifying the data on the site. Make sure you are only modifying entities that are safe to do so with.**

Updating an entity requires knowing the type and id, and passing the fields and values you want to update as a dictionary.
```python
# Set's the status of the Shot with id 123 to "final"
sg.update("Shot", 123, {"sg_status_list": "fnl"})
```

## Delete
**WARNING: This operation is actually modifying the data on the site. Make sure you are only modifying entities that are safe to do so with.**

Delete an entity just requires the type and id. Be VERY careful when deleting entities.

```python
success = sg.delete("Shot", 123)
# True
```

## Batch
**WARNING: This operation is actually modifying the data on the site. Make sure you are only modifying entities that are safe to do so with.**

Runs multiple actions in one query. When you run a shotgun method it has to connect to shotgun's server somewhere else in the world, run the method, then return the result. It takes time for the data to travel to and from the server, so batching helps by sending multiple requests in one go. Useful if you know all the arguments for the commands in advance.

```python
batch_requests = [
    {"request_type": "create", "entity_type": "Asset", "data": {"code": "myAsset", "sg_asset_type": "Prop"}},
    {"request_type": "update", "entity_type": "Asset", "entity_id": 123, "data": {"sg_status_list": "ip"}},
    {"request_type": "delete", "entity_type": "Asset", "entity_id": 456},
]
results = sg.batch(batch_requests)
```
