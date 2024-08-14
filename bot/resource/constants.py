class ReplyMessage:
    WELCOME: str = (
        "Bienvenue dans le serveur Discord de l'ASETIN.\n"
        "Afin de confirmer que vous êtes bel et bien un(e) étudiant(e) inscrit(e) à l'association, entrez votre numéro d'identification personnel (NI) via la commande !register [NI].\n"
        "Au plaisir de vous rencontrer!\n"
        "PS: Si vous ne savez pas où trouver votre NI, cliquez [ici](https://monportail.ulaval.ca/portail/carte-identite/apercus-carte).\n"
        "En tout temps, écrivez !help [NOM DE LA COMMANDE] pour connaître les options qui s'offrent à vous."
    )

    UNSUCCESSFUL_GENERIC: str = "Oh oh... quelque chose s'est mal passé."

    ALREADY_REGISTERED: str = (
        "Vous êtes déjà enregistré(e). Si vous ne vous êtes pas encore enregistré, veuillez contacter un administrateur."
    )

    UNABLE_TO_REGISTER: str = (
        "Impossible de vous enregistrer. Vérifiez votre NI. Si votre NI est le bon, veuillez contacter un administrateur."
    )

    UNABLE_TO_ADD_STUDENT: str = (
        "Impossible d'ajouter l'étudiant à la base de données. Vérifiez les arguments. Si le problème persiste, contactez la personne en charge du bot."
    )

    SUCCESSFUL_REGISTRATION: str = (
        "Vous êtes maintenant enregistré(e) ! Vous avez pleinement accès au serveur Discord."
    )

    SUCCESSFUL_FORCE_REGISTRATION: str = (
        "L'étudiant a bien été enregistré. Son rôle ainsi que son nom sont désormais affichés."
    )

    SUCCESSFUL_STUDENT_ADDED: str = (
        "Étudiant ajouté ! Il peut maintenant s'inscrire lui-même en m'envoyant un message privé."
    )

    SUCCESSFUL_FORCE_UNREGISTER: str = "L'utilisateur a été supprimé avec succès."

    STUDENT_ALREADY_EXISTS: str = "Cet étudiant existe déjà."

    STUDENT_NOT_FOUND: str = (
        "Cet étudiant n'existe pas dans notre systeme. Veuillez contacter un administrateur."
    )

    MISSING_ARGUMENTS_IN_COMMAND: str = "Arguments manquants dans la commande."

    NOTIFY_UNREGISTER: str = (
        "Vous avez été désinscrit(e) du serveur de l'ASETIN. Contactez un administrateur pour plus d'informations si vous n'avez pas effectué cette commande."
    )

    INVALID_FORMAT: str = "Un des arguments n'est pas dans le bon format."

    USER_NOT_IN_SERVER: str = "Action impossible, vous n'êtes pas sur le serveur."
