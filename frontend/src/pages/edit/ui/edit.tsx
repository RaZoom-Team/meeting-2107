import { useContext, useState } from 'react'
import styles from './style.module.scss'
import { addNotify, Card } from '../../../shared'
import { ReactSVG } from 'react-svg'
import PencilToSquareIcon from '@gravity-ui/icons/svgs/pencil-to-square.svg';
import {SealCheck} from '@gravity-ui/icons';
import { Button, Icon } from '@gravity-ui/uikit'
import { UserContext } from '../../../app/providers'
import { ModalEdit } from './modal_edit';
import { ModalAbout, ModalName, ModalClass } from './modals';
import { CropWidget } from '../../../widgets';
import { editUser, updateAvatar, User } from '../../../entities';
import { sendVerify } from '../api/api';

interface Props {
    verifySend: boolean
    verify_hook: React.Dispatch<React.SetStateAction<boolean>>
}

export function Edit({verifySend, verify_hook}: Props) {
    const [animEdit, setAnimEdit] = useState(false)
    const [editModal, setEdit] = useState(false)
    const [isCrop, setCrop] = useState(false)
    const [img, setImg] = useState<string | undefined>(undefined)
    const {user, setUser} = useContext(UserContext)

    const openModal = (func: React.Dispatch<React.SetStateAction<boolean>>) => {
        setEdit(false)
        func(true)
        setAnimEdit(false)
    }

    const onClose = () => {
        setEdit(false)
        setAnimEdit(false)
    }

    const imgUpload = (img: string) => {
        setImg(img)
        setCrop(true)
    }

    const [litera, setLitera] = useState(false)
    const [desc, setDesc] = useState(false)
    const [name, setName] = useState(false)

    const onEdit = () => {
        setAnimEdit(true)
        setEdit(true)
    }

    const onVerify = () => {
        sendVerify().then(() => {
            addNotify({
                title: 'Заявка отправлена',
                content: 'Заявка на верификацию успешно отправлена. Мы пришлем тебе уведомление после её рассмотрения',
                type: 'info'
            })
            verify_hook(true)
        })
    }

    const afterPhoto = (user: User) => {
        addNotify({
            title: 'Фото обновлено',
            content: 'Вы успешно обновили фотографию своего профиля'
        })
        setUser(user)
        setImg(undefined)
    }

    const onPhoto = (img: string | undefined) => {
        if (img) {
            fetch(img)
                .then(res => res.blob())
                .then(blob => {
                    const avatarForm = new FormData();
                    avatarForm.append('avatar', blob)
                    updateAvatar(avatarForm).then(afterPhoto)
                    setAnimEdit(false)
                })
            }
    }

    const offProfile = () => {
        if (user) editUser({
            ...user, 
            is_active: !user.is_active
        })
        .then((newUser: User) => {
            setUser(newUser)
            onClose()
            addNotify({
                title: 'Профиль '+(newUser.is_active ? 'активирован' : 'деактивирован'),
                content: 'Вы успешно '+(newUser.is_active ? 'активировали' : 'деактивировали')+' свой профиль'
            })
        })
    }

    if (img && user && isCrop){
    return  <CropWidget
                img={img}
                setImg={onPhoto}
                onComplete={() => setCrop(false)}
            />
    } else if (user) {
        return <main className={styles['main']}>

        <ModalEdit
        is_open={editModal} 
        open_litera={() => openModal(setLitera)}
        open_desc={() => openModal(setDesc)}
        open_name={() => openModal(setName)}
        set_photo={imgUpload}
        close_hook={onClose}
        is_active={user.is_active}
        profile_on_off={offProfile}
        />

        <ModalAbout is_open={desc} close_hook={() => setDesc(false)} nowDesc={user.desc}></ModalAbout>
        <ModalName is_open={name} close_hook={() => setName(false)} nowName={user.name} nowSur={user.surname}></ModalName>
        <ModalClass is_open={litera} close_hook={() => setLitera(false)} nowClass={user.literal}></ModalClass>
            <div className={styles['container']}>
            <Card 
                focus={user}
                is_me_liked={false}
                >
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
            <div style={(verifySend || user.verify) ? { display: 'none'} : {}} className={styles['button-container']}>
                <Button onClick={onVerify} pin='circle-circle' view='normal' size='m'>
                    <Icon data={SealCheck}></Icon>
                    Верификация
                </Button>
            </div>
        </div>
    </main>
    }
}