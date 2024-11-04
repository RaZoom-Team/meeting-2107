import { FocusUser} from "../../entities";
import { Feed, Edit, History } from "../../pages";
import { Page } from "../ui/app";

interface Props {
    page: Page
    focus: FocusUser
}

export function Router({page, focus}: Props) {
    const nowPage = () => {
        switch (page) {
            case 'feed':
                return <Feed focus={focus}/>
            case 'edit':
                return <Edit/>
            case 'history':
                return <History/>
        }
    }
    return nowPage()
}