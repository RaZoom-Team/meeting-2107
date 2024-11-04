import { useContext, useState } from 'react'
import styles from './style.module.scss'
import { Card } from '../../../shared'
import { ReactSVG } from 'react-svg'
import PencilToSquareIcon from '@gravity-ui/icons/svgs/pencil-to-square.svg';
import {SealCheck} from '@gravity-ui/icons';
import { Button, Icon, useToaster, Text } from '@gravity-ui/uikit'
import { UserContext } from '../../../app/providers'
import { ModalEdit } from './modal_edit';
import { ModalAbout, ModalName, ModalClass } from './modals';

export function Edit() {
    const [animEdit, setAnimEdit] = useState(false)
    const [editModal, setEdit] = useState(false)

    const {add, remove} = useToaster()
    const {user} = useContext(UserContext)

    const openModal = (func: React.Dispatch<React.SetStateAction<boolean>>) => {
        setEdit(false)
        func(true)
        setAnimEdit(false)
        
    }

    const [litera, setLitera] = useState(false)
    const [desc, setDesc] = useState(false)
    const [name, setName] = useState(false)

    const onEdit = () => {
        setAnimEdit(true)
        setEdit(true)
    }

    const onVerify = () => {
        const contentVerify = <div className={styles['toaster-container']}>
            <Text>Заявка на верификацию отправлена. Мы пришлем уведомление, если вы пройдете её</Text>
            <Button size='l' onClick={() => remove('verify')}>Понятно</Button>
        </div>
        add({
            title: 'Верификация',
            content: contentVerify,
            name: 'verify'
        })
    }
    if (user)
    return <main className={styles['main']}>
            <ModalEdit
            is_open={editModal} 
            open_litera={() => openModal(setLitera)}
            open_desc={() => openModal(setDesc)}
            open_name={() => openModal(setName)}
            close_hook={() => setEdit(false)}
            />

        <ModalAbout is_open={desc} close_hook={() => setDesc(false)} nowDesc={user.desc}></ModalAbout>
        <ModalName is_open={name} close_hook={() => setName(false)} nowName={user.name} nowSur={user.surname}></ModalName>
        <ModalClass is_open={litera} close_hook={() => setLitera(false)} nowClass={user.literal}></ModalClass>
            <div className={styles['container']}>
            <Card 
                name={focus.name}
                surname={user.surname}
                avatar={user.attachments[0]}
                desc={user.desc}
                litera={user.literal}
                is_me_liked={false}
                is_verify={user.verify}>
            </Card>
            <div className={styles['button-list']}>
                <button className={styles['button']}>
                    <ReactSVG
                    className={`${styles['icon']} ${animEdit ? styles['active-edit'] : styles['edit-icon']}`}
                    src={PencilToSquareIcon}
                    onClick={onEdit}
                    />  
                </button>
            </div>
        </div>
        <div className={styles['bottom-widget-container']}>
            <div className={styles['button-container']}>
                <Button onClick={onVerify} pin='circle-circle' view='normal' size='m'>
                    <Icon data={SealCheck}></Icon>
                    Верификация
                </Button>
            </div>
        </div>
    </main>
}