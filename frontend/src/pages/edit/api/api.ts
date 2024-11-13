import { UserClient } from "../../../shared";

export async function sendVerify() {
    UserClient.post('/verify')
    .then((response) => {
        return response.data
    })
    .catch((error) => {
        throw error
    })
}