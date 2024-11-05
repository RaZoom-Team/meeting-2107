import { Button, Select, Sheet } from "@gravity-ui/uikit"
import { AddNotify, Literales } from "../../../../shared"
import { useContext, useState } from "react"
import { UserContext } from "../../../../app/providers"
import { editUser } from "../../../../entities"
import styles from './style.module.scss'

interface Props {
    nowClass: string
    is_open: boolean
    close_hook: () => void
}

export function ModalClass({nowClass, is_open, close_hook}: Props) {
    const [litera, setLitera] = useState([nowClass])
    const {user, setUser} = useContext(UserContext)

    const onClass = () => {
        if (user){
        const newUser = {...user}
        newUser.literal = litera[0]
        editUser(newUser).then(newData => {
            setUser(newData)
            close_hook()
            AddNotify({
                title: 'Успешно',
                content: 'Класс был успешно изменён'
            })
        })
    }
    }

    return <Sheet title='Выберите класс' visible={is_open} onClose={close_hook}>
    <div className={styles['content']}>
        <Select className={styles['select-container']} width='max' label='Класс:' size="l" value={litera} defaultValue={litera} multiple={false} filterable={true} onUpdate={setLitera}>
            {Literales.map(option => <Select.Option key={option.key} value={option.value}>{option.value}</Select.Option>)}
        </Select>
        <div className={styles['button-list']}>
            <Button onClick={onClass} width="max" size="l">Применить</Button>
            <Button onClick={close_hook} width="max" view="outlined" size="l">Закрыть</Button>
        </div>
    </div>
</Sheet>
}