import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.reasoner.rulesys.*;
import com.hp.hpl.jena.query.*;
import java.util.*;
/** Uji aturan Jena (hasil konversi SWRL) dengan GenericRuleReasoner; jalankan query SPARQL dari file. */
public class JenaRulesTest {
  public static void main(String[] a) throws Exception {
    long t0 = System.currentTimeMillis();
    Model base = ModelFactory.createDefaultModel();
    base.read("file:" + a[0]);
    List<Rule> rules = Rule.rulesFromURL("file:" + a[1]);
    GenericRuleReasoner r = new GenericRuleReasoner(rules);
    InfModel inf = ModelFactory.createInfModel(r, base);
    inf.prepare();
    System.out.println("RULES=" + rules.size() + " BASE=" + base.size() + " INF=" + inf.size() + " ms=" + (System.currentTimeMillis() - t0));
    String q = new String(java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(a[2])), "UTF-8");
    for (String part : q.split("(?m)^#=+")) {
      String body = part.trim(); if (!body.contains("SELECT")) continue;
      String title = body.split("\n")[0];
      System.out.println("\n### " + title);
      QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(body), inf);
      ResultSet rs = qe.execSelect();
      System.out.print(ResultSetFormatter.asText(rs));
    }
  }
}
