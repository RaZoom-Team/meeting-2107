import styles from './style.module.scss'

interface Props {
    value: string
    hook: (value: string) => void,
    maxLength: number
}

export function TextArea({value, hook, maxLength}: Props) {
    return <textarea maxLength={maxLength} value={value} onChange={e => hook(e.target.value)} className={styles['textarea']}></textarea>
}

TextArea.defaultProps = {
    maxLength: undefined
}