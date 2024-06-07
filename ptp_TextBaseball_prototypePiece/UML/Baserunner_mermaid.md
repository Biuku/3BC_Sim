# Baserunner -- Mermaid diagram

```mermaid

flowchart 

    RMR(reset master rights)
    UR(update rights) 
    AF(advance fwd)
    AB(attain base)
    SR(score run)
    RF(remove force)
   
    UR --> RMR

    AF --> AB
    AB --> SR
    SR --> RMR
    AF --> RMR

    RF --> UR


```

