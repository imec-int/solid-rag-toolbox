---
sidebar_position: 2
---

# Scopes, Policies and Permissions

In this setup the policies, scopes, permissions and resources are automatically created on startup of the Keycloak service. These are all focused on the use cases of our 3 personae (see [Introduction](../intro.md)).
For each of these users policies are created on different types of their personal data. The following if an overview of all the different policies that are created to access the data of Adam.

- `calendar-adam@psx.be`: Access to Adam's calendar.
- `financial-adam@psx.be`: Access to Adam's financial information.
- `medical-adam@psx.be`: Access to Adam's medical information.
- `emails-adam@psx.be`: Access to Adam's e-mails.
- `notes-adam@psx.be`: Access to Adam's notes and todos.

All these different policies wil be created for each user. By default users have access on each other calendar, but not on any of the other types.

## Scopes

Scopes can be added to create a link between permissions/policies and resources for certain users. The scopes should be created first and will be used in the later steps when adding policies and permissions.

![Keycloak scopes overview](./img/keycloak_scopes.png)
_Keycloak scopes overview of Authz-service_

## Policies

Policies define the rules and conditions under which access to resources is granted. They determine who can access what data and under what circumstances. You can configure policies based on _list of users_, _user roles_, _time based_ access and other conditions. In our current setup we used list of users to define the policies.

![Keycloak policies overview](./img/keycloak_policies.png)
_Keycloak policies overview of Authz-service_

## Permissions

Permissions are scope-based to reflect the actual permissions of a user on a certain scope and policy. Permissions are linked to the policies and scopes. They have the final word on whether you have access or not; without permissions, access is not handled.

![Keycloak permissions overview](./img/keycloak_permissions.png)
_Keycloak permissions overview of Authz-service_
