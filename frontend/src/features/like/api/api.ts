import { User } from "../../../entities";
import { UserClient } from "../../../shared";
import { UserLove } from "../model/model";

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

export async function getLikes (): Promise<UserLove[]> {
    return UserClient.get('/likes')
    .then(response => {
        return response.data;
    })
    .catch(error => {
        console.log(error)
        throw error
    })
} 
