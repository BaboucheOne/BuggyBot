class ReplyMessage:
    WELCOME: str = (
        "Bienvenue dans le serveur Discord de l'ASETIN.\n"
        "Afin de confirmer que tu es bel et bien un(e) étudiant(e) inscrit(e) à l'association, entre ton numéro d'identification personnel (NI) via la commande !register [NI].\n"
        "Au plaisir de te rencontrer!\n"
        "PS: Si tu ne sais pas où trouver ton NI, clique [ici](https://monportail.ulaval.ca/portail/carte-identite/apercus-carte).\n"
        "En tout temps, écris !help pour connaître les options qui s'offrent à toi."
    )

    UNSUCCESSFUL_GENERIC: str = "Oh oh... quelque chose s'est mal passé."

    ALREADY_REGISTERED: str = (
        "Vous êtes déjà enregistré. Si vous ne vous êtes pas encore enregistré, veuillez contacter un administrateur."
    )

    UNABLE_TO_REGISTER: str = (
        "Impossible de vous enregistrer. Vérifiez votre NI. Si votre NI est le bon, veuillez contacter un administrateur."
    )

    SUCCESSFUL_REGISTRATION: str = (
        "Vous êtes maintenant enregistré(e)! Votre rôle ainsi que votre nom sont désormais enregistrés."
    )

    SUCCESSFUL_STUDENT_ADDED: str = (
        "Étudiant ajouté ! Il peut maintenant s'inscrire lui-même en m'envoyant un message privé."
    )

    SUCCESSFUL_UNREGISTER: str = "L'utilisateur a été désenregistré avec succès."

    STUDENT_ALREADY_EXISTS: str = "Cet étudiant existe déjà."

    MISSING_ARGUMENTS_IN_COMMAND: str = "Arguments manquants dans la commande."

    NOTIFY_UNREGISTER: str = (
        "Vous avez été désenregistré du serveur ASETIN. Contactez un administrateur pour plus d'informations."
    )
