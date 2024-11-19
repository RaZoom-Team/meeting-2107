import { User } from "../../../entities";
import { UserClient } from "../../../shared";

export async function register(data: FormData): Promise<User> {
    return UserClient.post('', data).then(response => {
        return response.data;
    }).catch(error => {
        throw error;
    });
} 