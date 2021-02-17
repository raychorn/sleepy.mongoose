## Sleepy.Mongoose via Flask on steroids.

### About

This is a reimagination of the original Sleepy Mongoose that used to work with Python 2.x but this one works with Python 3.x and was developed with Python 3.9.1.

### Connect

```
POST http://127.0.0.1:27080/_connect/ HTTP/1.1
content-type: application/json

{
    "MONGO_URI": "172.27.107.98:27017",
    "MONGO_INITDB_ROOT_USERNAME": "root",
    "MONGO_INITDB_ROOT_PASSWORD": "put your password here",
    "MONGO_INITDB_DATABASE": "admin",
    "MONGO_AUTH_MECHANISM": "SCRAM-SHA-256"
}

```

### list_databases

```
GET http://localhost:27080/list_databases/ HTTP/1.1

```

### list_collections

```
GET http://localhost:27080/_use/WORD-CLOUD/list_collections HTTP/1.1

```

### count_documents

```
GET http://localhost:27080/_use/WORD-CLOUD/articles/count_documents HTTP/1.1

```

### find

```
GET http://localhost:27080/_use/WORD-CLOUD/articles/find HTTP/1.1

```

See [the wiki](https://github.com/10gen-labs/sleepy.mongoose/wiki) for documentation.

(c). Copyright, Ray C Horn, All Rights Reserved.
