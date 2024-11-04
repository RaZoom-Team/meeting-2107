import styles from './style.module.scss'
import { Button, Sheet, TextInput } from "@gravity-ui/uikit"
import { ReactElement} from "react"

interface Props {
    is_open: boolean
    close_hook: () => void
    func_hook: () => void
    content: string
    content_hook: React.Dispatch<React.SetStateAction<string>>
}

export function ModalReport({is_open, close_hook, func_hook, content, content_hook}: Props): ReactElement {
    
    return <Sheet title='Жалоба' visible={is_open} onClose={close_hook}>
        <div className={styles['content']}>
            <TextInput view='normal' value={content} onChange={(e) => content_hook(e.target.value)} size="l" type="text" placeholder="Напишите сюда причину жалобы" autoFocus={true}></TextInput>
            <Button width='max' onClick={func_hook} size="l" view='normal'>Пожаловаться</Button>
        </div>
    </Sheet>
}