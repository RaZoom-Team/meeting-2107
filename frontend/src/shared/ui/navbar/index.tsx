import styles from './style.module.scss'
import { ReactSVG } from 'react-svg'

interface Props {
    buttons: NavIcon[]
}

export type NavIcon = {
    src: string
    hook: () => void
    active: boolean
}

export function NavBar({buttons}: Props) {

    const buttonsList = buttons.map(button => {
        return <button key={button.src} data-active={button.active ? 'YES' : 'NO'} className={styles['icon-button']} onClick={button.hook}>
            <ReactSVG
            data-active={button.active ? 'YES' : 'NO'}
            className={styles['icon']}
            src={button.src}/>
        </button>
    })

    return <nav className={styles['navigation-bar']}>
            {buttonsList}
        </nav>
}