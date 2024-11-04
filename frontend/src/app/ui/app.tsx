import styles from './style.module.scss'
import { useContext, useState} from 'react'
import {Auth} from '../../pages'
import { UserContext } from '../providers'
import { editIcon, feedIcon, historyIcon, NavBar, NavIcon } from '../../shared'
import { Router } from '../router/router'
import { ReactNotifications } from 'react-notifications-component'
import { ThemeProvider, ToasterComponent, ToasterProvider } from '@gravity-ui/uikit'

export type Page = 'feed' | 'history' | 'edit'

export function App() {
  const {user} = useContext(UserContext)
  const [page, setPage] = useState<Page>('feed')

  if (user === undefined) {
    return <>Загрузка</>
  } 
  else if (user === null) {
    return <Auth/>
  } 
  else {

    const buttons: NavIcon[] = [
      {src: editIcon, hook: () => setPage('edit'), active: page == 'edit'},
      {src: feedIcon, hook: () => setPage('feed'), active: page == 'feed'},
      {src: historyIcon, hook: () => setPage('history'), active: page == 'history'},
    ]

    return <ThemeProvider theme='dark'>
            <ToasterProvider>
          <ToasterComponent mobile={true}></ToasterComponent>

      <main data-theme={user.male ? 'blue' : 'pink'} className={styles['main']}>
        <ReactNotifications></ReactNotifications>
        <NavBar buttons={buttons}/>
        <Router page={page} focus={user.focus_user}/>
    </main>
    </ToasterProvider>
    </ThemeProvider>

  }
}

