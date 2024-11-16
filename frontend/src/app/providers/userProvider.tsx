import { createContext, Dispatch, ReactNode, SetStateAction, useEffect, useState } from "react";
import { getUser, User } from "../../entities";
import { AxiosError } from "axios";
import { BanPage, ChannelPage } from "../../pages";

interface IChildren {
    children: ReactNode;
}

interface Props {
    user: User | undefined | null;
    updateUser: () => void;
    setUser: Dispatch<SetStateAction<User | null | undefined>>;
}

export const UserContext = createContext<Props>({} as Props);

export default function UserProvider({ children }: IChildren) {

    const [user, setUser] = useState<User | undefined | null>(undefined);
    const [isSub, setSub] = useState(true)
    const [link, setLink] = useState('')
    const [ban, setBan] = useState('')

    const updateUser = () => {
        setUser(undefined)
        getUser()
        .then(setUser)
        .catch(
            (error: AxiosError) => {
            if (error.response?.data) {
                console.log(error.response.headers)
                const statusCode = (error.response.data as {code: number}).code.toString()
                console.log(statusCode)
                if (statusCode == '3004') {
                    setSub(false)
                    setLink(error.response.headers['x-channel'])
                    console.log(error.response.headers)
                } else if (statusCode == '3005') {
                    setBan(decodeURI(error.response.headers['x-reason']))
                }

            }
            setUser(null)
        })
    }

    useEffect(() => {
        updateUser();
    }, []);

    useEffect(() => {
        console.log(user)
    }, [user])


    
        return (
        <UserContext.Provider value={{ user, updateUser, setUser }}>
            {isSub ? children : <ChannelPage link={link} />}
            {ban.length > 0 && <BanPage reason={ban} link={"https://t.me/pudsluhano_man"}/>}
        </UserContext.Provider>
    );
}