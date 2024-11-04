import { Button, Icon, ToasterComponent, useToaster, Text } from '@gravity-ui/uikit';
import '../../../app/index.scss';
import styles from './style.module.scss';
import {SealCheck, CardHeart} from '@gravity-ui/icons';

interface Props {
    name: string;
    surname: string;
    avatar: string;
    litera: string;
    desc: string;
    is_me_liked: boolean
    is_verify: boolean
}

export function Card({ name, surname, avatar, desc, litera, is_me_liked, is_verify}: Props) {
    const {add, remove} = useToaster()
    const contentVerify = 
    <div className={styles['toaster-container']}>
        <Text>Данные этого пользователя подтверждены администрацией  <Icon data={SealCheck}></Icon></Text>
        <Button size='l' onClick={() => remove('verify')}>Понятно</Button>
    </div>

    const contentLike = 
        <div className={styles['toaster-container']}>
            <Text>Этот пользователь лайкнул вас  <Icon data={CardHeart}></Icon></Text>
            <Button size='l' onClick={() => remove('like')}>Понятно</Button>
        </div>

    const onVerify = () => {
        add({
            title: 'Верифицирован',
            content: contentVerify,
            name: 'verify'
        });
    }

    const onLike = () => {
        add({
            title: 'Симпатия',
            content: contentLike,
            name: 'like'
        });
    }

    <ToasterComponent></ToasterComponent>

    return (
        <div className={styles['bg']} style={{ background: `linear-gradient(180.00deg, rgba(0, 0, 0, 0.85) 0%,rgba(0, 0, 0, 0) 60.239%), url(${avatar})`}}>
            <div className={styles['card']}>
                <div className={styles['overlay']}>
                    <div className={styles['upper-container']}>
                    <span className={styles['name']}>{surname} {name}</span>
                    <div className={styles['status-list']}>
                        {!is_verify  ? <Button onClick={onVerify} pin='circle-circle'><Icon data={SealCheck}/></Button> : <></>}
                        {!is_me_liked ? <Button onClick={onLike} pin='circle-circle'><Icon data={CardHeart}/></Button> : <></>}
                        </div>
                    </div>
                    <div className={styles['about']}>
                        <section className={`${styles['section']} ${styles['section-class']}`}>
                            <span className={styles['section-title']}>Класс</span>
                            <span className={`${styles['section-text']} ${styles['class-text']}`}>{litera}</span>
                        </section>
                        <section className={`${styles['section']} ${styles['section-desc']}`}>
                            <span className={styles['section-title']}>О себе</span>
                            <span className={`${styles['section-text']} ${styles['desc-text']}`}>{desc}</span>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    );
}