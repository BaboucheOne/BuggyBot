class ReplyMessage:
    WELCOME: str = (
        "Bienvenue dans le serveur Discord de l'ASETIN (Association des étudiantes et étudiants en informatique)! \n"
        "Afin de confirmer que tu es bel et bien un(e) étudiant(e) inscrit(e) à l'association, entre ton numéro d'identification personnel (NI).\n"
        "Au plaisir de te rencontrer!\n"
        "ps: Si tu ne sais pas où trouver ton NI, tu peux le consulter sur MonPortail ou encore sur ta carte étudiante."
    )

    HELP: str = (
        "All my available commands:\n"
        "1.`!register [NI]` -> Register you to access channels.\n"
        "2.`!asetin` to have info on this association.\n"
        "3.`!aeglo` to have info on this association."
    )

    UNSUCCESSFUL_GENERIC: str = "Oh oh... something went wrong."

    ALREADY_REGISTERED: str = (
        "Your are already registered.\nIf you haven't registered yet, please contact an admin."
    )

    UNABLE_TO_REGISTER: str = (
        "Unable to registered you.\nCheck your NI. If your NI is the good one, please contact an admin."
    )

    SUCCESSFUL_REGISTRATION: str = (
        "You are now registered! Your role is now apply and your name is set."
    )

    SUCCESSFUL_STUDENT_ADDED: str = (
        "Student added ! He can now registered my himself by sending me a dm."
    )

    SUCCESSFUL_UNREGISTER: str = "user has been successfully unregistered."

    STUDENT_ALREADY_EXISTS: str = "This student already exists."

    MISSING_ARGUMENTS_IN_COMMAND: str = "Missing arguments in the command."

    NOTIFY_UNREGISTER: str = (
        "You have been unregistered from ASETIN's server. Contact an admin for more info."
    )
