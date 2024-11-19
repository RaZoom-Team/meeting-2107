import styles from './style.module.scss'

interface Props {
    hook: (value: string) => void
    value: string,
    maxLength: number
}

export function Input({value, hook, maxLength}: Props) {
    return <input maxLength={maxLength} className={styles['input']} type={'text'} value={value} onChange={e => hook(e.target.value)}/>
}

Input.defaultProps = {
    maxLength: undefined
}