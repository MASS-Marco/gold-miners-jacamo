package mining;

/** Casos pequenos com gabarito manual para a base do tutorial. */
public class ModelChecks {
    static int checks = 0;
    static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
        checks++;
    }
    public static void main(String[] args) throws Exception {
        WorldModel.destroy();
        WorldModel w = WorldModel.create(4,4,2);
        w.setDepot(0,0);
        w.setAgPos(0,1,1);
        w.setAgPos(1,2,1);
        w.add(WorldModel.GOLD,1,1);
        w.add(WorldModel.GOLD,1,2);
        w.add(WorldModel.OBSTACLE,0,1);
        w.move(MiningPlanet.Move.LEFT,0);
        check(w.getAgPos(0).x==1 && w.getAgPos(0).y==1,"atravessou obstaculo");
        w.move(MiningPlanet.Move.RIGHT,0);
        check(w.getAgPos(0).x==1,"sobreposicao de agentes");
        check(w.pick(0) && w.isCarryingGold(0),"coleta nao ocorreu");
        check(!w.hasObject(WorldModel.GOLD,1,1),"ouro duplicado apos coleta");
        w.move(MiningPlanet.Move.DOWN,0);
        check(!w.pick(0) && w.hasObject(WorldModel.GOLD,1,2),"capacidade excedida");
        w.move(MiningPlanet.Move.RIGHT,0);
        check(w.drop(0) && w.getGoldsInDepot()==0 && w.hasObject(WorldModel.GOLD,2,2),"descarte fora do deposito");
        check(w.pick(0),"nova coleta");
        w.setAgPos(0,0,0); // fixture coloca o agente no destino; a integracao testa o caminho real.
        check(w.drop(0) && w.getGoldsInDepot()==1 && !w.isCarryingGold(0),"deposito incorreto");
        check(!w.drop(0) && w.getGoldsInDepot()==1,"pontuacao duplicada");
        check(w.countObjects(WorldModel.GOLD)+w.getGoldsInDepot()==2,"conservacao do ouro");
        System.out.println("GOLD_MINERS|MODEL_CHECKS|passed="+checks);
    }
}
