import { Button, Icon} from '@gravity-ui/uikit';
import '../../../app/index.scss';
import styles from './style.module.scss';
import {SealCheck, CardHeart} from '@gravity-ui/icons';
import { addNotify } from '../notify';

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

    const onVerify = () => {
        addNotify({
            title: 'Верифицирован',
            content: 'Данные этого пользователя подтверждены администрацией',
            type: 'utility'
        });
    }

    const onLike = () => {
        addNotify({
            title: 'Симпатия',
            content:'Этот пользователь лайкнул вас',
            type: 'utility'
        });
    }

    return (
        <div className={styles['bg']} style={{ background: `linear-gradient(180.00deg, rgba(0, 0, 0, 0.85) 0%,rgba(0, 0, 0, 0) 60.239%), url(${avatar}) no-repeat center center`}}>
            <div className={styles['card']}>
                <div className={styles['overlay']}>
                    <div className={styles['upper-container']}>
                    <span className={styles['name']}>{surname} {name}</span>
                    <div className={styles['status-list']}>
                        {is_verify  ? <Button onClick={onVerify} pin='circle-circle'><Icon data={SealCheck}/></Button> : null}
                        {is_me_liked ? <Button onClick={onLike} pin='circle-circle'><Icon data={CardHeart}/></Button> : null}
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