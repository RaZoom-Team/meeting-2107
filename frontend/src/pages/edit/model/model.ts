import { User } from "../../../entities";

export type UserEdit = Omit<User, 'focus_user' | 'focus_is_liked'> 