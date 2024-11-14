import { useState } from "react";
import { FocusUser} from "../../entities";
import { Feed, Edit, History } from "../../pages";
import { Page } from "../model/page";

interface Props {
    page: Page
    focus: FocusUser
}

export function Router({page, focus}: Props) {
    const [verifySend, setVerify] = useState(false)

    const nowPage = () => {
        switch (page) {
            case Page.FEED:
                return <Feed focus={focus}/>
            case Page.EDIT:
                return <Edit verifySend={verifySend} verify_hook={setVerify}/>
            case Page.HISTORY:
                return <History/>
        }
    }
    return nowPage()
}