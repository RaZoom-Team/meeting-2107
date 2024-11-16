import styles from './style.module.scss'
import { ReactElement, useContext, useEffect, useState } from "react";
import { Sex, Stage } from "../model/types";
import {Input, Button, Select, Option, InputImg, TextArea,  white2107, blue2107, pink2107, Literales, addNotify, ErrorsText } from '../../../shared';
import { CropWidget } from '../../../widgets';
import { UserContext } from '../../../app/providers';
import { register } from '../api/api';
import {AxiosError } from 'axios';

export function Auth() {


    const {updateUser} = useContext(UserContext)
    const [theme, setTheme] = useState<'pink' | 'blue' | null>(null)
    const [stage, setStage] = useState<Stage>(Stage.SUBINFO)
    const [name, setName] = useState<string>('')
    const [surname, setSurname] = useState<string>('')
    const [sex, setSex] = useState<string>('')
    const [image, setImage] = useState<string | undefined>(undefined)
    const [desc, setDesc] = useState<string>('')
    const [literal, setLiteral] = useState<string|null>(null)

    useEffect(() => {
        switch (sex) {
            case Sex.MALE:
                setTheme('blue')
                break
            case Sex.WOMAN:
                setTheme('pink')
                break
            default:
                break
        }
    }, [sex])


    const Sexs: Option[] = [
        {key: "male", value: "Мужчина"},
        {key: "woman", value: "Женщина"}
    ]

    const inputName = 
    <div className={styles["input-list"]}>
        <div className={styles['input-block']}>
            <span className={styles['title']}>Имя</span>
            <Input value={name} hook={setName}></Input>
        </div>
        <div className={styles['input-block']}>
            <span className={styles['title']}>Фамилия</span>
            <Input value={surname} hook={setSurname}></Input>
        </div>
    </div>

    const inputSex = 
    <div className={styles["input-list"]}>
        <div className={styles['input-block']}>
            <span className={styles['title']}>Выберите пол</span>
            <Select value={sex || ''} options={Sexs} title='Пол' hook={setSex}/>
        </div>
        <div className={styles['input-block']}>
            <span className={styles['title']}>Выберите класс</span>
            <Select value={literal || ''} options={Literales} title='Класс' hook={setLiteral}/>
        </div>
    </div>

    const [isCropping, setCropping] = useState(true)
    const startCropping = (img: string) => {
        setImage(img)
        setCropping(true)
    }
    const inputImg = <div className={styles["input-list"]}>
            <div className={styles['input-block']}>
                    <span className={styles['title']}>Ваше фото</span>
                    <InputImg src={image} hook={startCropping}/>
            </div>
        </div>

    const inputAbout =
    <div className={styles["input-list"]}>
        <div className={styles['input-block']}>
            <span className={styles['title']}>О себе</span>
            <TextArea value={desc} hook={setDesc}/>
        </div>
    </div>

    const inputNow = (): ReactElement => {
        switch (stage) {
            case Stage.NAME:
                return inputName;
            case Stage.SUBINFO:
                return inputSex
            case Stage.PHOTO:
                return inputImg
            case Stage.ABOUT:
                return inputAbout
            default:
                return inputName;
        }
    }

    const imgNow = () => {
        switch (theme) {
            case 'blue':
                return blue2107
            case 'pink':
                return pink2107
            default:
                return white2107
        }
    }

    const checkActive = (): boolean => {
        if (stage == Stage.SUBINFO && literal && sex) {
            return true
        } else if (
            stage == Stage.NAME &&
            name.length > 2 &&
            surname.length > 2 &&
            (name.split(' ').length == 1 || (name.split(' ').length > 1 && name.split(' ')[1] == '' && name.split(' ')[name.split(' ').length-1] == '')) &&
            (surname.split(' ').length == 1 || (surname.split(' ').length > 1 && surname.split(' ')[1] == '' && surname.split(' ')[surname.split(' ').length-1] == '')))
        {
            return true
        } else if (stage == Stage.PHOTO && image) {
            return true
        } else if (stage == Stage.ABOUT && desc.length >= 4) {
            return true
        } else {
            return false;
        }
    }

    const submitUser = () => {
        if (image) {
            fetch(image)
                .then(res => res.blob())
                .then(blob => {
                    console.log(blob)
                    setName((name) => name.trim())
                    setSurname((surname) => surname.trim())
                    // const userData: UserRegister = {
                    //     name,
                    //     surname,
                    //     male: sex === Sex.MALE,
                    //     desc,
                    //     literal: literal ? literal : ''
                    // };
                    const userData = new FormData();
                    userData.append('avatar', blob)
                    userData.append('name', name)
                    userData.append('surname', surname)
                    userData.append('male', sex === Sex.MALE ? "true" : "false")
                    userData.append('desc', desc)
                    userData.append('literal', literal ? literal : '')
                    register(userData)
                    .then(updateUser)
                    .catch((error: AxiosError) => {
                        console.log(error)
                        if (error.response?.data) {
                            const statusCode = (error.response.data as {code: number}).code.toString()
                            if (statusCode in ErrorsText) {
                                addNotify({
                                    title: 'Упс...',
                                    content: ErrorsText[statusCode],
                                    btn_text: 'Перейти в канал',
                                    btn_hook: () => Telegram.WebApp.openTelegramLink(error.response?.headers['X-Channel']),
                                    type: "danger"
                                })
                            }
                            else {
                                addNotify({
                                title: 'Упс...',
                                content: statusCode, 
                                type: "danger"
                                })
                            }
                        }
                    })
                })
            }
    }

    if (stage == Stage.PHOTO && isCropping && image) {
        return <CropWidget
        img={image}
        setImg={setImage}
        onComplete={() => setCropping(false)}
    />
    }
    else {
        return <main data-theme={theme} className={styles['main']}>
        {stage != Stage.PHOTO ? <img className={styles['logo']} src={imgNow()}></img> : <></>}
        {inputNow()}
        <section className={styles['buttons']}>
            {stage == Stage.ABOUT ? 
            <Button text='Отправить' hook={submitUser} active={checkActive()}/>
            : <Button text='Продолжить' hook={() => setStage(stage + 1)} active={checkActive()}/>
            }
            <Button text='Назад' style='outfill' hook={() => setStage(stage - 1)} active={stage > 0}/>
        </section>
    </main>
    }
}