while not self.partida2:
    dt = self.clock.tick(FPS)
    self.ct += dt
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    
    print(nave.rect.x)
    #movimiento original fondo pantalla
    self.bgMove1()  
    self.screen.blit(self.planeta1.image, (self.planeta1.rect.x, self.planeta1.rect.y))
    
    #mete en el grupo de sprites de Meteoritos la cantidad de meteoritos max expecificada.
    if self.ct >= 2000:

        for x in range(self.maxMeteo):
            self.meteoritos.add(meteors.Meteor(DIMENSIONS[0] - 32, random.randint(150, DIMENSIONS[1] - 32)))
        self.ct = 0    

    #va mostrando en pantalla los meteoritos y los elimina si pasan de cierta posición en pantalla
    for meteor in self.meteoritos:
        self.screen.blit(meteor.image, (meteor.rect.x, meteor.rect.y))

        if meteor.rect.x < -meteor.rect.w:
            self.meteoritos.remove(meteor)
            self.meteorsDodge += 1
            self.puntuacion += 50
            self.SPuntuacion = self.pointText.render(f":{self.meteorsDodge}", True, (255,255,255))
            self.Spunt = self.pointText.render(f":{self.puntuacion}", True, (255,255,255))

    #reinicio los atributos de los meteoritos        
    #self.puntuacion = 0 #<--- quitar después de pruebas 
    self.maxMeteo = 2
    self.meteoritos.update()
    self.naves.update()

    #mostrar vidas en pantalla
    x = 500
    for vida in range(self.vidas):
        self.screen.blit(self.vidasimg, (x, 75))
        x += 50
    

    for nave in self.naves:
        if nave.status == ship.Status.aterrizando:
            self.screen.blit(nave.naveRotadaS, (nave.naveRotadaRect.x, nave.naveRotadaRect.y))

        else:
            self.screen.blit(nave.image, (nave.rect.x, nave.rect.y))

        
    self.screen.blit(self.menu.image, (self.menu.rect.x, self.menu.rect.y))
    self.screen.blit(self.SPuntuacion, (self.RPuntuacion.x, self.RPuntuacion.y))
    self.screen.blit(self.Spunt, (self.Rpunt.x, self.Rpunt.y))
    

    if self.RPuntuacion.y < 50 and self.Rpunt.y < 50:
        self.RPuntuacion.y += 1
        self.Rpunt.y += 1
    else:
        pass

    #calcula la colisión de 2 grupos de sprites, nave y meteo, y si detecta colisión elimina el meteorito
    if self.puntuacion < 600:
        if pg.sprite.groupcollide(self.naves, self.meteoritos, False, True):
            for nave in self.naves:
                nave.status = ship.Status.explotando
                self.vidas -= 1
            self.puntuacion -= 25
            self.reset()
        
    #mira si la puntuación a llegado al limite y saca el planeta por la parte derecha y elimina los meteoritos    
    if self.puntuacion >= 600:
        self.maxMeteo = 0
        for meteor in self.meteoritos:
            if meteor.rect.x < -80:
                self.meteoritos.remove(meteor)
        
        if nave.status != ship.Status.aterrizando:        
            nave.status = ship.Status.aterrizando    #<---- mirar el orden para ponerlo                  
        self.planeta1.update()
    

    if nave.status == ship.Status.aterrizada:
        print("entra")
        self.screen.fill((0,0,0))

        textofin = self.textoTitulo.render("GAME COMPLETE", True, (255,255,255))
        textofinRect = textofin.get_rect(center=(self.dimensionsBg1.centerx //4, 200))
        textoScore = self.textoTitulo.render(f"TU PUNTUACIÓN ES DE: {self.puntuacion}", True, (255,255,255))
        textoScoreRect = textoScore.get_rect(center=(self.dimensionsBg1.centerx //4, 400))
        self.screen.blit(textofin, (textofinRect.x, textofinRect.y))
        self.screen.blit(textoScore, (textoScoreRect.x, textoScoreRect.y))

    
    pg.display.flip()