import styles from './style.module.scss'
import { FocusUser, User } from "../../../entities";
import { AddNotify, Card } from '../../../shared';
import { ReactSVG } from 'react-svg';
import { useContext, useRef, useState } from 'react';
import { UserContext } from '../../../app/providers';
import gsap from 'gsap'
import { useGSAP } from '@gsap/react';
import { likeSend } from '../../../features/like';
import { Button, Icon } from '@gravity-ui/uikit';
import {ShieldExclamation} from '@gravity-ui/icons';
import { ModalReport, reportSend } from '../../../features';
import HeartFillIcon from '@gravity-ui/icons/svgs/heart-fill.svg';
import XmarkIcon from '@gravity-ui/icons/svgs/xmark.svg';

gsap.registerPlugin(useGSAP);

interface Props {
    focus: FocusUser | null
}

export function Feed({focus}: Props) {
    const [animLike, setLike] = useState(false);
    const [animClose, setClose] = useState(false);
    const [animReport, setanimReport] = useState(false);
    const [bg, setBg] = useState(true);
    const card = useRef<HTMLDivElement>(null);
    const newData = useRef<User | null | undefined>(null)
    const {user, setUser} = useContext(UserContext)
    const [reportModal, setReportModal] = useState<boolean>(false)
    const [reportContent, setReportContent] = useState<string>('')

    useGSAP(
        () => {
            if (animLike && card.current) {
                newData.current = undefined
                likeSend(true).then((data) => {
                    newData.current = data
                    //console.log("загрузил")
                })
                const afterData = () => {
                    while (!newData) { console.log(newData) }
                    setUser(newData.current)
                    newData.current = null
                    setLike(false)
                    const tlGet = gsap.timeline()
                    tlGet.fromTo(card.current, {x: 500, y: 0}, {x: 0, duration: 0.8, ease: 'power1'})
                    tlGet.fromTo(card.current, {scale: 0.8}, {x: 0, scale: 1, duration: 0.4, ease: 'power1', onComplete: () => setBg(true)})
                }
                const tlSend = gsap.timeline({onComplete: afterData})
                tlSend.to(card.current, {y: -20, duration: 0.3, ease: 'power1', onComplete: () => setBg(false)})
                tlSend.to(card.current, {scale: 0.8, duration: 0.4, ease: 'power1'}, '<')
                tlSend.to(card.current, {x: -500, duration: 0.8, ease: 'slow'}, '>')
            }
        }, [animLike])

        useGSAP(
            () => {
                if (animClose && card.current) {
                    newData.current = undefined
                    likeSend(false).then((data) => {
                        newData.current = data
                        //console.log("загрузил")
                    })
                    const afterData = () => {
                        while (!newData) { console.log(newData) }
                        setUser(newData.current)
                        newData.current = null
                        setClose(false)
                        const tlGet = gsap.timeline()
                        tlGet.fromTo(card.current, {x: 500}, {x: 0, duration: 0.8, ease: 'power1'})
                        tlGet.fromTo(card.current, {scale: 0.8}, {x: 0, scale: 1, duration: 0.4, ease: 'power1', onComplete: () => setBg(true)})
                    }
                    const tlSend = gsap.timeline({onComplete: afterData})
                    tlSend.to(card.current, {y: -20, duration: 0.3, ease: 'power1', onComplete: () => setBg(false)})
                    tlSend.to(card.current, {scale: 0.8, duration: 0.4, ease: 'power1'}, '<')
                    tlSend.to(card.current, {x: -500, duration: 0.8, ease: 'slow'}, '>')
                }
            }, [animClose])
        useGSAP(
            () => {
                if (animReport && card.current) {
                    const tlSend = gsap.timeline()
                    tlSend.to(card.current, {y: -20, duration: 0.3, ease: 'power1', onComplete: () => setBg(false)})
                    tlSend.to(card.current, {scale: 0.8, duration: 0.4, ease: 'power1'}, '<')
                    tlSend.to(card.current, {x: -500, duration: 0.8, ease: 'slow'}, '>')

                    setUser(newData.current)

                    const tlGet = gsap.timeline()
                    tlGet.fromTo(card.current, {x: 500}, {x: 0, duration: 0.8, ease: 'power1'})
                    tlGet.fromTo(card.current, {scale: 0.8}, {x: 0, scale: 1, duration: 0.4, ease: 'power1', onComplete: () => setBg(true)})
                    newData.current = null
                    setanimReport(false)
                }
            }, [animReport])
    

    const onReport = () => {
        reportSend(reportContent).then(dataAfterReport => {
            setReportModal(false)
            newData.current = dataAfterReport
            setanimReport(true)
            AddNotify({
                title: 'Заявка отправлена',
                content: 'Жалоба на этого пользователя успешно отправлена администраторам',
                type: 'info'
            })
        })
    }

    if (!focus) {
        <main data-bg={"NO"} className={styles['main']}>
    </main>
    } else if (user) return <main data-bg={bg ? "YES" : "NO"} className={styles['main']}>
        <ModalReport func_hook={onReport} content={reportContent} content_hook={setReportContent} is_open={reportModal} close_hook={() => setReportModal(false)}></ModalReport>
        <div ref={card} className={styles['container']}>
            <Card name={focus.name} surname={focus.surname} avatar={focus.attachments[0]} desc={focus.desc} litera={focus.literal} is_me_liked={user.focus_is_liked} is_verify={focus.verify}></Card>
            <div className={styles['button-list']}>
                <button className={styles['button']}>
                    <ReactSVG
                    className={`${styles['icon']} ${animLike ? styles['active-like'] : styles['like']}`}
                    src={HeartFillIcon}
                    onClick={() => setLike(true)}
                    />  
                </button>
                <button className={styles['button']}>
                    <ReactSVG
                    className={`${styles['icon']} ${animClose ? styles['active-close'] : styles['close']}`}
                    src={XmarkIcon}
                    onClick={() => setClose(true)}
                    />
                </button>
            </div>
        </div>
        <div className={styles['bottom-widget-container']}>
            <div className={styles['button-container']}>
                <Button onClick={() => setReportModal(true)} pin='circle-circle' view='normal' size='m'>
                    <Icon data={ShieldExclamation}></Icon>
                    Пожаловаться
                </Button>
            </div>
        </div>
    </main>
}