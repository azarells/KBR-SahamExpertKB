import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.assembler.Assembler;
import com.hp.hpl.jena.query.*;
import com.hp.hpl.jena.update.*;
import com.hp.hpl.jena.util.FileManager;
/** Uji bagian ja: dari config Fuseki + what-if SPARQL Update pada InfModel. */
public class AssemblerTest {
  static void q(Model m, String s) { QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(s), m); System.out.print(ResultSetFormatter.asText(qe.execSelect())); }
  public static void main(String[] a) throws Exception {
    Model spec = FileManager.get().loadModel("file:" + a[0], "TURTLE");
    Resource rInf = null, rPel = null;
    for (ResIterator it = spec.listSubjects(); it.hasNext();) { Resource r = it.next(); if (r.isURIResource()) { if (r.getURI().endsWith("#infSaham")) rInf = r; if (r.getURI().endsWith("#modelPellet")) rPel = r; } }
    System.out.println("root=" + rInf);
    Model live = (Model) Assembler.general.open(rInf);
    Model pel = (Model) Assembler.general.open(rPel);
    System.out.println("live=" + live.size() + " pellet=" + pel.size());
    String P = "PREFIX ex: <http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#>\n";
    String Q = P + "SELECT ?stres ?regime ?k WHERE { ex:Pasar_ID_Okt2026 ex:skorStresPasar ?stres ; ex:regimeTerdeteksi ?regime ; a ?k . FILTER(?k IN (ex:DivergensiIntermarketBullish, ex:ZonaAkumulasiGenerasional, ex:StrategiAkumulasiBertahap)) }";
    String T = P + "SELECT ?t WHERE { ?t a ex:TesisTerpicu }";
    System.out.println("== SEBELUM what-if"); q(live, Q); q(live, T);
    System.out.println("== pellet dataset top pick adaptif"); q(pel, P + "SELECT (COUNT(?e) AS ?n) WHERE { ?e a ex:KandidatTopPickAdaptif }");
    String u = new String(java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(a[1])), "UTF-8");
    UpdateAction.parseExecute(u, live);
    System.out.println("== SESUDAH what-if"); q(live, Q); q(live, T);
  }
}
