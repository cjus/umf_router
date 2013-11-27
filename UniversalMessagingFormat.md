# Universal Messaging Format

## 1. Introduction
This specification describes an application-level messaging format suitable for use with WebSockets and in traditional HTTP JSON payloads. The proposed message format is designed as a replacement format for what is already in use and to potentially accommodate future requirements. From this point forward we’ll refer to the Universal Messaging Format as UMF.

We’ll also refer to UMFs as documents because they can be stored in memory, transmitted along communication channels and retained in offline storage.

## 2. Message Format
The UMF is a valid JSON document that is required to validate with existing JSON validators and thus be fully compliant with the JSON specification.

Example validators:

* [Curious Concept JSON formatter](http://jsonformatter.curiousconcept.com)
* [JSON Editor Online](http://www.jsoneditoronline.org)

JSON Specification: http://www.json.org/

JSON is a data interchange format based on JavaScript Object Notation. As such, UMF which is encoded in JSON, follows well established JavaScript naming conventions. For example, UMF retains the use of camel case for compound names.

### 2.1 Envelope format
UMF uses an envelope format where the outer portion is a valid JSON object and the inner portion consist of directives (headers) and a message body. Variations of this approach is used in the SOAP XML format where the outer portion is called an envelope and the inner portion contains both header and body sections. In other formats headers and body may be side by side as is the case of HTTP.

In UMF the inner portion consists of UMF reserved key/value pairs with an optional body object

    {
      "mid": "ef5a7369-f0b9-4143-a49d-2b9c7ee51117",
      "rmid": "66c61afc-037b-4229-ace4-5ec4d788903e",
      "to": "uid:123",
      "from": "uid:56",
      "type": "dm",
      "version": "1.0",
      "priority": "10",
      "timestamp": "2013-09-29T10:40Z",
      "body": {
        "message": "What’s up yo?"
      }
    }


Only UMF reserved words may be used. However, application specific (custom) key/value pairs may be used freely inside the body value.  This strict requirement ensures that the message format has a strict agreed upon format as defined by it’s version number.

## 2.2 Reserved Fields
As described earlier UMF consists of reserved key/value pairs with an optional embedded body object.  This section describes each of the reserved fields and their intended use. A reserved field consists of a name key followed by a value which is encoded in a strict format. As we’ll see later in this specification, only the body field differs from this requirement.  The point here is that a reserved field has a value content which follows a strict format.

### 2.2.1 Mid field (Message ID)
Each message must contain an mid field with a universally unique identifier (UUID) as a value. 

For example:

    {
    :
    "mid":"ef5a7369-f0b9-4143-a49d-2b9c7ee51117"
    }

The mid field is required to uniquely identify a message across multiple applications, services and replicated servers. All programming environments support the use of UUIDs. 

* AS3: https://code.google.com/p/actionscript-uuid/
* Python: import uuid
* JavaScript: http://www.javascriptoo.com/uuid-v4-js  

Because UMF is an asynchronous message format, an individual message may be generated on either a server or client application. Each is required to create a UUID for use with a newly created message.

The mid field is a required field.
  
### 2.2.2 Rmid field (Refers to Message ID)
The Refers to Message ID (rmid) is a method of specifying that a message refers to another message.  The use of the rmid field is helpful in the case of a message that requires reply or where a reply finalizes or changes an application's state machine. This is also useful in threaded conversations there a message may be sent in reply to another pre-existing message.

The rmid field is NOT a required field.
 
### 2.2.3 To field (routing)
The to field is used to specify message routing.  A message may be routed to other users, internal application handlers or to other remote servers.

The value of a to field is a colon or forward slash separated list of sub names.

For example:

    {
      :
      "to":"server:service"
    }

specifies that the message should be routed to a server called server and a service called service.  Another example would be a message which is intended to be routed to a specific user:

    {
      :
      "to":"UID:143"
    }

Sending a message to a user’s inbox might look like this:

    {
      :
      "to":"UID:143:inbox"
    }

The use of the colon (:) or forward slash (/) separator is intended to simplify parsing using the split function available in string parsing libraries. Colon and forward slash may not be used in the same key value, however their use may differ across messages. Keep in mind that the value of a to field may not be a single entity but rather a broadcasting service which sends the message to various subscribers.

The to field is a required field and must be present in all messages.
 
2.2.4 From field (routing)

The from field is used to specify a source during message routing.  Like the to field, the value of a from field is a colon or forward slash separated list of sub names.

For example:

    {
      :
      "from":"server:service"
    }

specifies that the message should be routed to a server called server and a service called service.  Another example would be a message which is intended to be routed to a specific user:

    {
      :
      "from":"UID:64"
    }

The use of the colon (:) or forward slash (/) separator is intended to simplify parsing using the split function available in string parsing libraries. Colon and forward slash may not be used in the same key value, however their use may differ across messages.

The from field is a required field and must be present in all messages. 
 
### 2.2.5 Type field (message type)
The message type field describes a message as being of a particular classification.

The type field is a NOT a required field.  If type missing from a message, a type of msg is assumed:

    {
      :
      "type":"msg"
    }

An application developer may choose to implement a sub message type inside of their message’s body object.

    {
      :
      "body":{
        "type":"chat",
        "message":"What’s up yo?"
      }
    }

However, the message will still be handled as a generic message (msg) by other servers and infrastructure components which may or may not inspect the contents of the custom body object.  For this reason it’s recommended that standard type fields be used whenever possible.


The following message types are envisioned as part of this draft specification: 
 
#### 2.2.5.1 im (instant message)
A message type of im refers to an instant message.  This is a message from one user to another and may or may not be private.  Determination is deferred to the implementing application.

#### 2.2.5.2 dm (direct message)
Identifies a message as being a direct message message type.  These are private messages  sent from one user to another user.

#### 2.2.5.3 chat (chat message)
Identifies a message as being a chat message type. A chat message is one sent to one or more users within a group or room.

#### 2.2.5.4 inbox
Whenever a message can’t be delivered to a user (perhaps because they’re no longer online) an application which implements the UMF may decide to store undelivered message in a user’s inbox.  The application may allow users to send “email” type messages to one or more user inboxes by detecting the presence of the “type”: “inbox” message.

#### 2.2.5.5 Note on extending message types
It’s expected that adding message types will be required to adopt UMF in existing products. The recommended guideline is to extend types with generic types which are considered universal across all products. Where a type is product specific it should only be introduced inside of the user-level body object and not made part of the UMF specification.  This restriction is designed to maintain the usefulness of UMF without polluting it with key/values pairs which follow no rhyme nor reason.

### 2.2.6 Version field
UMF messages have a version field that identifies the version format for a given message.

    {
      :
      "version": "1.0"
    }

The version value format is of the form of “major version . minor version . revision version”
“...the major number is increased when there are significant jumps in functionality, the minor number is incremented when only minor features or significant fixes have been added, and the revision number is incremented when minor bugs are fixed.” http://en.wikipedia.org/wiki/Software_versioning

Applications implementing UMF may choose to only consider the major and minor version segments, ignoring the revision version.

The version field is a required field, must be present in all messages and is required to include both a major and minor version number.

### 2.2.7 Priority field
UMF documents may include an optional priority field.  If not present a default value equal to default priority is assumed. If present, priority field values are in the range of 10 (highest) to 1 (lowest).  

Normal priority is valued at 5.
 
    {
      :
      "priority": "10"
    }

In addition to numeric values the strings “low”,”normal”,”high” may be used to indicate message priorities:

    {
      :
      "priority": "high"
    }

The priority field is NOT a required field and defaults to “normal” priority if unspecified.

### 2.2.8 Timestamp field
UMF supports a timestamp field which indicates when a message was sent. The format for a timestamp is ISO 8601, a standard date format. http://en.wikipedia.org/wiki/ISO_8601 

When using an ISO 8601 formatted timestamp, UMF requires that the time be in the UTC timezone.

    {
      :
      "timestamp":"2013-09-29T10:40Z",
    }

All programming environments include support for converting local machine time to UTC.

There are a number of reasons why message timestamps are useful:
* Communication can be ordered chronologically during display, searching and storage.
* Messages past a set time can be handled differently, including being purged from a system.

The timestamp field is a required UMF field.

### 2.2.9 Ttl field (time to live)
The ttl field is used to specify how long a message may remain alive within a system. The value of this field is an amount of time specified in seconds.

    {
      :
      "ttl": "300"
    }

The ttl field is optional and if not present in a UMF document the default is a ttl which never expires.
 
### 2.2.10 Body field (application level data)
The body field is used to host an application-level custom object.  This is where an application may define message content which is meaningful in the context of its application.

    {
      "mid": "ef5a7369-f0b9-4143-a49d-2b9c7ee51117",
      "to": "uid:56",
      "from": "game:store",
      "version": "1.0",
      "timestamp": "2013-09-29T10:40Z",
      "body": {
        "type": "store:purchase",
        "itemID": "5x:winnings:multiplier",
        "expiration": "2014-02-10T10:40Z"
      }
    }

In the example above a user receives confirmation of a purchase (power-up item) from the game store, the items can then be added to the user’s inventory.
 
#### 2.2.9.1 Overriding UMF restricted key / value pairs
As mentioned earlier UMF restricted fields may not be used in occurrence to this specification, however, an application may override UMF restricted fields by including those fields in its custom body object.

The following are potential usecases:

* The application may choose to include it’s own sub-routing and override the to and from fields.
* It might be desirable to have an application level message version
* The application may require it’s own message id (mid) format

The application level code is free to override the meaning of UMF restricted keys by looking inside its body object for potential overrides.
 
#### 2.2.9.2 Sending binary data
Binary or encrypted / encoded messages may be sent via the UFM by using a JSON compatible data convertor such as Base64 http://en.wikipedia.org/wiki/Base64 

When using a converter the base format should be indicated in a user level field such as “contentType” whose value should be a standard Internet Media Type (formally known as a MIME type) http://en.wikipedia.org/wiki/Internet_media_type
 
    {
      "mid": "ef5a7369-f0b9-4143-a49d-2b9c7ee51117",
      "to": "uid:134",
      "from": "uid:56",
      "version": "1.0",
      "timestamp": "2013-09-29T10:40Z",
      "body": {
        "type": "private:message",
        "contentType": "text/plain",
        "base64": "SSBzZWUgeW91IHRvb2sgdGhlIHRyb3VibGUgdG8gZGVjb2RlIHRoaXMgbWVzc2FnZS4="
      }
    }

In this way, audio and images may be transmitted via UMF.
 
#### 2.2.9.3 Sending multiple application messages
An application may, for efficiency reasons, decide to bundle multiple sub-messages inside of a single UMF document. The recommended method of doing this to define a body object which contains one or more sub messages.

    {
      "mid": "ef5a7369-f0b9-4143-a49d-2b9c7ee51117",
      "to": "uid:134",
      "from": "bingo:room:14",
      "version": "1.0",
      "timestamp": "2013-09-29T10:40Z",
      "body": {
        "type": "chat:messages",
        "messages": [
          {
            "msg": {
              "from": "moderator",
              "text": "Susan welcome to Bingo Nation NYC",
              "ts": "2013-09-29T10:34Z"
            },
           "msg": {
             "from": "uid:16",
             "text": "Rex, you are one lucky SOB!",
             "ts": "2013-09-29T10:30Z"
            },
           "msg": {
             "from": "uid:133",
             "text": "Rex you're going down this next round",
             "ts": "2013-09-29T10:31Z"
           }
         }
        ]
      }
    }

In the example above messages consists of an array of objects.
 
# 3. Use inside of HTTP
UMF documents may be sent via HTTP request and responses.  Proper use requires setting HTTP content header, Content-Type: application/javascript

    POST http://server.com/api/v1/message HTTP/1.1
    Host: server.com
    Content-Type: application / javascript; charset=utf-8
    Content - Length:length

    {
      "mid": "ef5a7369-f0b9-4143-a49d-2b9c7ee51117",
      "rmid": "66c61afc-037b-4229-ace4-5ec4d788903e",
      "to": "uid:123",
      "from": "uid:56",
      "type": "dm",
      "version": "1.0",
      "priority": "10",
      "timestamp": "2013-09-29T10:40Z",
      "body": {
        "message": "What’s up yo?"
      }
    }

# 4. Peer-to-Peer Communication
UMF documents may be used to exchange P2P messages between distributed services.  One example of this would be a service which sends its application health status to a monitoring and data aggregation service. 

For example:

    {
      "mid": "ef5a7369-f0b9-4143-a49d-2b9c7ee51117",
      "to": "stats:server",
      "from": "bingo:server:23",
      "version": "1.0",
      "priority": "10",
      "timestamp": "2013-09-29T10:40Z",
      "body": {
        "totalRooms": "200",
        "averageUsersPerRoom": "13",
        "averageRoomStay": "1200"
      }
    }

In the example above bingo game server #23 is sending a message to the stats:server indicating it’s stats at UTC 2013-09-29T10:40Z.
 
# 5. Infrastructure considerations

## 5.1 Message storage
UMF is designed with distributed servers in mind. The use of mid’s (unique message IDs) allows messages to be stored by their message id in servers such as Redis, MongoDB and in legacy databases.

## 5.2 Message routing
The use of the UMF to and from fields support message routing. The implementation of message routers is deferred to UMF implementers.  The use of colon and forward slash separators is intended to allow routes to easily parse for target handlers.

### 5.2.1 Message forwarding
It’s possible to route message between (through) servers by implementing message forwarding. 

For example:

    {
      :
      "mid": "ef5a7369-f0b9-4143-a49d-2b9c7ee51117",
      "to": "router:uk-router:bingo:room:12"
    }

The message above might be sent to a router (service) which then parses the to field and realizes that the message is intended for a UK server. So it forwards the message to the uk-router which in turn sends the message to a bingo server which hosts room 12.
 
# 6. Optimizations
The WebSocket protocol accepts binary data. Converting JSON to binary format introduces efficiencies over classic string based JSON. The MongoDB NoSQL database makes extensive use of binary JSON, called BSON.

It’s possible to use BSON to encode UMF. There are libraries available for use with ActionScript3, Python.

* Search: “BSON in actionscript” and “Python BSON” for listings
