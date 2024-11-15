import axios from "axios";
import { API_URL } from "./config";

export const UserClient = axios.create({
    baseURL: API_URL+'/user',
})


UserClient.interceptors.request.use(config => {
    //config.headers['Tg-Authorization'] = Telegram.WebApp.initData;
    config.headers['Tg-Authorization'] = "user%3D%7B%22id%22%3A1977502575%2C%22first_name%22%3A%22Zoom%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22ramchike%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D%26chat_instance%3D6800930143016803379%26chat_type%3Dsender%26auth_date%3D1729890471%26hash%3Dc98f9da098efdb0e642fdfb9b078f5e8e5bf3fcbfeef932cfecc3e5b540502ec"
    return config
})

export const AttachmentsClient = axios.create({
    baseURL: API_URL+'/attachments'
})  