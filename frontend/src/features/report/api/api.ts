import { User } from "../../../entities";
import { UserClient } from "../../../shared";

export async function reportSend (reason: string): Promise<User> {
    return UserClient.post('/likes/report', {reason})
    .then(response => {
        return response.data
    })
    .catch(error => {
        console.log(error)
        throw error
    })
}