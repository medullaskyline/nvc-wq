define({
    "pages": {
        "login": {
            "url": "login",
            "name": "login"
        },
        "logout": {
            "url": "logout",
            "name": "logout"
        },
        "user": {
            "my_custom_flag": true,
            "lookup": "username",
            "can_add": false,
            "form": [
                {
                    "name": "username",
                    "label": "Username",
                    "bind": {
                        "required": true
                    },
                    "hint": "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                    "wq:length": 150,
                    "type": "string"
                },
                {
                    "name": "first_name",
                    "label": "First Name",
                    "wq:length": 30,
                    "type": "string"
                },
                {
                    "name": "last_name",
                    "label": "Last Name",
                    "wq:length": 30,
                    "type": "string"
                },
                {
                    "name": "email",
                    "label": "Email address",
                    "wq:length": 254,
                    "type": "string"
                },
                {
                    "name": "is_staff",
                    "label": "Is Staff",
                    "type": "boolean"
                },
                {
                    "name": "is_active",
                    "label": "Is Active",
                    "type": "boolean"
                },
                {
                    "name": "last_login",
                    "label": "Last Login",
                    "type": "dateTime",
                    "can_edit": false
                },
                {
                    "name": "date_joined",
                    "label": "Date Joined",
                    "type": "dateTime"
                }
            ],
            "cache": "filter",
            "name": "user",
            "url": "users",
            "list": true
        },
        "feeling": {
            "name": "feeling",
            "url": "feelings",
            "list": true,
            "form": []
        },
        "feelingsneedsentry": {
            "my_custom_flag": true,
            "cache": "filter",
            "name": "feelingsneedsentry",
            "url": "feelings-needsentries",
            "list": true,
            "form": [
                {
                    "name": "user",
                    "label": "User",
                    "bind": {
                        "required": true
                    },
                    "type": "string",
                    "wq:ForeignKey": "user"
                },
                {
                    "name": "feeling",
                    "label": "Feeling",
                    "bind": {
                        "required": true
                    },
                    "type": "string",
                    "wq:ForeignKey": "feeling"
                },
                {
                    "name": "need",
                    "label": "Need",
                    "bind": {
                        "required": true
                    },
                    "type": "string",
                    "wq:ForeignKey": "need"
                },
                {
                    "name": "notes",
                    "label": "Notes",
                    "type": "text"
                },
                {
                    "name": "public",
                    "label": "Public",
                    "choices": [
                        {
                            "name": "FALSE",
                            "label": "false"
                        },
                        {
                            "name": "TRUE",
                            "label": "true"
                        }
                    ],
                    "type": "select one"
                }
            ]
        },
        "need": {
            "name": "need",
            "url": "needs",
            "list": true,
            "form": []
        }
    }
});
