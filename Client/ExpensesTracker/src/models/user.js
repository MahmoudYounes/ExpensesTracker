export default class user{
    constructor(
        Id,
        password,
        lastLogin,
        isSuperUser,
        username,
        firstName,
        lastName,
        email,
        isStaff,
        isActive,
        dateJoined
    )
    {
        this.Id = Id;
        this.password = password;
        this.lastLogin = lastLogin
        this.isSuperUser = isSuperUser
        this.username = username
        this.firstName = firstName
        this.lastName = lastName
        this.email = email
        this.isStaff = isStaff
        this.isActive = isActive
        this.dateJoined = dateJoined
    }
}