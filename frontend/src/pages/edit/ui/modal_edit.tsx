import styles from './modal.module.scss'
import { Button, Sheet } from "@gravity-ui/uikit"
import { ReactElement} from "react"

interface Props {
    is_open: boolean
    close_hook: () => void
    open_litera: () => void
    open_desc: () => void
    open_name: () => void
 }

export function ModalEdit({is_open, close_hook, open_desc, open_litera, open_name}: Props): ReactElement {

    const onGender = () => {

    }

    const onPhoto = () => {

    }

    return <Sheet title='Редактировать' visible={is_open} onClose={close_hook}>


        <div className={styles['content']}>
            <div className={styles['button-list']}>
                <Button width='max' onClick={onGender} size="m" view='outlined'>Пол</Button>
                <Button width='max' onClick={open_desc} size="m" view='outlined'>О себе</Button>
                <Button width='max' onClick={open_litera} size="m" view='outlined'>Класс</Button>
                <Button width='max' onClick={open_name} size="m" view='outlined'>Имя фамилию</Button>
                <Button width='max' onClick={onPhoto} size="m" view='outlined'>Фотографию</Button>
            </div>
        </div>
    </Sheet>
}