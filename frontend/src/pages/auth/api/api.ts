import { User } from "../../../entities";
import { UserClient } from "../../../shared";
import { UserRegister } from "../model/types";

export async function register(user: UserRegister, avatar: FormData): Promise<User> {
    return UserClient.post('', avatar, {params: user}).then(response => {
        return response.data;
    }).catch(error => {
        throw error;
    });
} 