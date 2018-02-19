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
        "feelingmaincategory": {
            "cache": "all",
            "name": "feelingmaincategory",
            "url": "FeelingMainCategories",
            "list": true,
            "form": [
                {
                    "name": "feeling_sub_categories",
                    "label": "Feeling Sub Categories",
                    "bind": {
                        "required": true
                    },
                    "type": "repeat",
                    "children": [
                        {
                            "name": "feeling_leaves",
                            "label": "Feeling Leaves",
                            "bind": {
                                "required": true
                            },
                            "type": "repeat",
                            "children": []
                        }
                    ]
                }
            ]
        },
        "feelingsubcategory": {
            "cache": "all",
            "name": "feelingsubcategory",
            "url": "FeelingSubcategories",
            "list": true,
            "form": [
                {
                    "name": "feeling_leaves",
                    "label": "Feeling Leaves",
                    "bind": {
                        "required": true
                    },
                    "type": "repeat",
                    "children": []
                }
            ]
        },
        "needcategory": {
            "cache": "all",
            "name": "needcategory",
            "url": "NeedCategories",
            "list": true,
            "edit": false,
            "new": false,
            "form": [
                {
                    "name": "needleaves",
                    "label": "",
                    "bind": {
                        "required": true
                    },
                    "type": "group",
                    "children": [
                        {
                            "type": "string",
                            "name": "need_leaf",
                            "label": ""
                        }
                    ]
                }
            ]
        },
        "user": {
            "my_custom_flag": true,
            "lookup": "username",
            "can_add": false,
            "cache": "filter",
            "name": "user",
            "url": "users",
            "list": true,
            "fields": [
                "username",
                "first_name",
                "last_name",
                "email",
                "is_staff",
                "is_active",
                "last_login",
                "date_joined"
            ],
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
                    "label": "Staff status",
                    "hint": "Designates whether the user can log into this admin site.",
                    "type": "boolean"
                },
                {
                    "name": "is_active",
                    "label": "Active",
                    "hint": "Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                    "type": "boolean"
                },
                {
                    "name": "last_login",
                    "label": "Last Login",
                    "type": "dateTime"
                },
                {
                    "name": "date_joined",
                    "label": "Date Joined",
                    "type": "dateTime"
                }
            ]
        },
        "entry": {
            "my_custom_flag": true,
            "cache": "filter",
            "name": "entry",
            "url": "entries",
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
                    "name": "feeling_main_category",
                    "label": "Feeling Main Category",
                    "bind": {
                        "required": true
                    },
                    "type": "string",
                    "wq:ForeignKey": "feelingmaincategory"
                },
                {
                    "name": "feeling_sub_category",
                    "label": "Feeling Sub Category",
                    "bind": {
                        "required": true
                    },
                    "type": "string",
                    "wq:ForeignKey": "feelingsubcategory"
                },
                {
                    "name": "feeling",
                    "label": "Feeling",
                    "bind": {
                        "required": true
                    },
                    "type": "string",
                    "wq:ForeignKey": "feelingleaf"
                },
                {
                    "name": "need_category",
                    "label": "Need Category",
                    "bind": {
                        "required": true
                    },
                    "type": "string",
                    "wq:ForeignKey": "needcategory"
                },
                {
                    "name": "need",
                    "label": "Need",
                    "bind": {
                        "required": true
                    },
                    "type": "string",
                    "wq:ForeignKey": "needleaf"
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
        "needleaf": {
            "cache": "all",
            "list": true,
            "modes": [
                "list"
            ],
            "name": "needleaf",
            "url": "NeedLeaves",
            "form": []
        },
        "feelingleaf": {
            "cache": "all",
            "name": "feelingleaf",
            "url": "FeelingLeaves",
            "list": true,
            "form": []
        },
        "relationshiptype": {
            "name": "relationshiptype",
            "url": "relationshiptypes",
            "list": true,
            "form": [
                {
                    "name": "name",
                    "label": "Name",
                    "bind": {
                        "required": true
                    },
                    "wq:length": 255,
                    "type": "string"
                },
                {
                    "name": "inverse_name",
                    "label": "Inverse Name",
                    "wq:length": 255,
                    "type": "string"
                },
                {
                    "name": "from_type",
                    "label": "From Type",
                    "bind": {
                        "required": true
                    },
                    "type": "string"
                },
                {
                    "name": "to_type",
                    "label": "To Type",
                    "bind": {
                        "required": true
                    },
                    "type": "string"
                },
                {
                    "name": "computed",
                    "label": "Computed",
                    "type": "boolean"
                }
            ],
            "label_template": "{{name}}"
        }
    }
});
