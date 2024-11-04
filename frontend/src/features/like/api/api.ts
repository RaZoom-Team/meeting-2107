import { FocusUser, User } from "../../../entities";
import { UserClient } from "../../../shared";

export async function likeSend (status: boolean): Promise<User | null> {
    return UserClient.post('/likes', {status})
    .then(response => {
        return response.data;
    })
    .catch(error => {
        console.log(error)
        throw error
    })
}

export async function getLikes (): Promise<FocusUser[]> {
    return UserClient.get('/likes')
    .then(response => {
        return response.data;
    })
    .catch(error => {
        console.log(error)
        throw error
    })
} 
