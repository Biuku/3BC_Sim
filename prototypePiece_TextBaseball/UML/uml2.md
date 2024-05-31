# Mermaid diagram

```mermaid

flowchart 

    A(master do stuff)
    A --> SB(start BIP)
    A --> FB(finish BIP)
    A --> RRR(refresh runner rights)

    SB --> UF(update forced)
    SB <--> GOB(get occupied bases)
    FB --> AB(advance baserunner)
    FB --> RRR
    FB --> RS(reset situation)

    RRR <--> GOB
    RRR --> RF(remove forces)
    AB <--> RRR
    AB --> | advance fwd | BR[[BASERUNNER]]

    UF <--> GOB
    UF --> RB(reset bases)
    UF --> AF(apply force)
    AF --> |apply_forced| BR

```

<!--  NOTE I HAD TO REMOVE TRIANGLE BRACKETS AS ARROWS BELOW
    M[[MAIN]] -- A
    M -- U1(update primary user input)
    A -- SP(screen print)
    SP -- BOT(get base occupants text)
    SP -- GRT(get runner rights text)
    SP -- PR[[SCREENPRINTER]]
    M -- U2(update secondary user input)
    M -- USS(update start-stop user input)
    
    U2 -- UR(update runners to act user input)
>