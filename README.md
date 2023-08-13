# Little Lemon Backend API Documentation

## Paths, Methods and Authorizations

### Some `Djoser` default paths

```
/auth/users
```
```
/auth/users/users/me
```
```
/auth/token/login
```

For details, see [Djoser documentation](https://djoser.readthedocs.io/en/latest/index.html).

### Obtain token

```
/api-token-auth
```

| Methods | Parameters           | Data Type  | Authorized User Types |
| ------- | -------------------- | ---------- | --------------------- |
| `POST`  | username<br>password | str<br>str | Authenticated users   |

### List all menu items, create new menu item

```
/api/menu
```

| Methods | Parameters                  | Data Type                    | Authorized User Types |
| ------- | --------------------------- | ---------------------------- | --------------------- |
| `GET`   | None                        | None                         | All users             |
| `POST`  | title<br>price<br>inventory | str<br>float (2 d.p.)<br>int | Manager               |

### Retrieve, update, destroy single menu item

```
/api/menu/{menu_item_id}
```

| Methods  | Parameters    | Data Type  | Authorized User Types |
| -------- | ------------- | ---------- | --------------------- |
| `GET`    | None          | None       | All users             |
| `PATCH`  | Any           | Any        | Manager               |
| `DELETE` | None          | None       | Manager               |

### List all bookings, create new booking

```
/api/booking
```

| Methods | Parameters                           | Data Type                                     | Authorized User Types |
| ------- | ------------------------------------ | --------------------------------------------- | --------------------- |
| `GET`   | None                                 | None                                          | Authenticated users   |
| `POST`  | name<br>no_of_guests<br>date<br>time | str<br>int<br>str (yyyy-mm-dd)<br>str (hh:mm) | Authenticated users   |
