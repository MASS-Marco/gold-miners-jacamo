// Percurso fixo de verificacao. Nao e uma estrategia de competicao.
{ include("$jacamoJar/templates/common-cartago.asl") }
!verificar.

+!verificar
 <- !posicao(1,0);
    ?cell(1,1,gold);
    .print("GOLD_MINERS|PERCEPTION|gold=1,1");
    down;
    !posicao(1,1);
    pick;
    !com_carga;
    ?not cell(1,1,gold);
    .print("GOLD_MINERS|PICK|carrying=true");
    up;
    !posicao(1,0);
    left;
    !posicao(0,0);
    drop;
    !sem_carga;
    validateDelivery;
    .print("GOLD_MINERS|END|status=ok");
    .stopMAS.

+!posicao(X,Y) : pos(X,Y).
+!posicao(X,Y) : not pos(X,Y) <- .wait(20); !posicao(X,Y).
+!com_carga : carrying_gold.
+!com_carga : not carrying_gold <- .wait(20); !com_carga.
+!sem_carga : not carrying_gold.
+!sem_carga : carrying_gold <- .wait(20); !sem_carga.
-!verificar <- .print("GOLD_MINERS|FAIL|agent_verification"); .stopMAS.
