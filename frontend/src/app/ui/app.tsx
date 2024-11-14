import styles from './style.module.scss'
import { useContext, useEffect, useState} from 'react'
import {Auth} from '../../pages'
import { UserContext } from '../providers'
import { editIcon, feedIcon, historyIcon, NavBar, NavIcon, white2107 } from '../../shared'
import { Router } from '../router/router'
import { useSwipeable } from 'react-swipeable'
import { Page } from '../model/page'

export function App() {
  const {user} = useContext(UserContext)
  const [page, setPage] = useState<Page>(Page.FEED)

  const handlers = useSwipeable({
    onSwipedRight: (() => {
      if (page > 0) setPage((page) => page - 1)
    }),
    onSwipedLeft: (() => {
      if (page < 2) setPage((page) => page + 1)
    })
  })

  useEffect(() => {
    Telegram.WebApp.expand()
  }, [])

  if (user === undefined) {
    return <main className={styles['main']}>
      <div className={styles['load-container']}>
        <img style={{width: '200px'}} src={white2107}/>
      </div>
    </main>
  } 
  else if (user === null) {
    return <Auth/>
  } 
  else {

    const buttons: NavIcon[] = [
      {src: editIcon, hook: () => setPage(Page.EDIT), active: page == Page.EDIT},
      {src: feedIcon, hook: () => setPage(Page.FEED), active: page == Page.FEED},
      {src: historyIcon, hook: () => setPage(Page.HISTORY), active: page == Page.HISTORY},
    ]

    return  <main data-theme={user.male ? 'blue' : 'pink'} className={styles['main']} {...handlers}>
        <NavBar buttons={buttons}/>
        <Router page={page} focus={user.focus_user}/>
    </main>

  }
}

