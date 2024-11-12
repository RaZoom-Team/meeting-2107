import { UserClient } from "../../shared";
import { User } from "./model";

export async function getUser(): Promise<User|null> {
    return UserClient.get('')
    .then(
        response => {
            return response.data
        }
    ).catch(error => {
        console.log(error)
        throw error
    })
}

export async function editUser(newUser: User): Promise<User> {
    return UserClient.patch('', newUser).then(
        response => {
            return response.data
        }
    ).catch(error => {
        console.log(error)
        throw error
    })
}

export async function updateAvatar(avatar: FormData) {
    return UserClient.patch('/avatar', {avatar})
    .then(response => {
        return response.data
    }).catch(error => {
        console.log(error)
        throw error
    })
} 

export async function genKey (username: string): Promise<string> {
    return UserClient.post('/getauth', {username})
    .then(
        response => {
            return response.data
        }
    ).catch(error => {
        console.log(error)
        throw error
    })
}