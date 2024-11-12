import styles from './modal.module.scss'
import { Button, Sheet } from "@gravity-ui/uikit"
import { ReactElement, useContext, useRef } from "react"
import { UserContext } from '../../../app/providers'
import { addNotify } from '../../../shared'
import { editUser } from '../../../entities'

interface Props {
    is_open: boolean
    close_hook: () => void
    open_litera: () => void
    open_desc: () => void
    open_name: () => void
    set_photo: React.Dispatch<React.SetStateAction<string | undefined>>
}

export function ModalEdit({is_open, close_hook, open_desc, open_litera, open_name, set_photo}: Props): ReactElement {

    const {user, setUser} = useContext(UserContext)
    const fileInputRef = useRef<HTMLInputElement | null>(null)

    const onGender = () => {
        if (user) {
            const newUser = {...user}
            newUser.male = !user.male
            editUser(newUser).then(newData => {
                setUser(newData)
                close_hook()
                addNotify({
                    title: 'Успешно',
                    content: ('Пол успешно изменен на ' + (newUser.male ? 'мужской' : 'женский'))
                })
            })
        }
    }

    const imgChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            set_photo(URL.createObjectURL(e.target.files[0]))
        }
        close_hook()
    }

    const handlePhotoClick = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click()
        }
    }

    return (
        <Sheet title='Редактировать' visible={is_open} onClose={close_hook}>
            <div className={styles['content']}>
                <div className={styles['button-list']}>
                    <Button width='max' onClick={onGender} size="m" view='outlined'>Пол</Button>
                    <Button width='max' onClick={open_desc} size="m" view='outlined'>О себе</Button>
                    <Button width='max' onClick={open_litera} size="m" view='outlined'>Класс</Button>
                    <Button width='max' onClick={open_name} size="m" view='outlined'>Имя фамилию</Button>
                    <Button width='max' onClick={handlePhotoClick} size="m" view='outlined'>Фотографию</Button>
                    <input 
                        type="file" 
                        ref={fileInputRef} 
                        style={{ display: 'none' }} 
                        onChange={imgChange} 
                    />
                </div>
                <Button width='max' onClick={close_hook} size="l">Закрыть</Button>
            </div>
        </Sheet>
    )
}